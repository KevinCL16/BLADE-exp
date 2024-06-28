import os
import traceback
import os.path as osp
from typing import Union
from blade_bench.data.annotation import AnnotationDBData
from blade_bench.data.datamodel.transforms import TransformDatasetState
from blade_bench.data.load_annotation import load_ground_truth_data
from blade_bench.eval.convert import Convert
from blade_bench.eval.datamodel.lm_analysis import (
    EntireAnalysis,
    EntireAnalysisProcessed,
)
from blade_bench.eval.exceptions import (
    LMSubmissionConversionError,
    RunError,
    LoadGroundTruthError,
    MatchAnnotationsError,
    GetMetricsError,
)
from blade_bench.eval.datamodel.match import MatchedAnnotations
from blade_bench.eval.datamodel.result import EvalResult
from blade_bench.eval.match.match_submission import SubmissionMatch
from blade_bench.eval.metrics.all_metrics import get_metrics_from_match_obj
from blade_bench.eval.utils import SAVE_CONVERTED_CODE_TEMPLATE
from blade_bench.llms.base import TextGenerator
from blade_bench.llms.datamodel.gen_config import LLMHistory
from blade_bench.logger import logger
from blade_bench.eval.datamodel.run import RunResultModes, EvalRunResults
from blade_bench.eval.datamodel.submission import DatasetSubmission

from blade_bench.utils import get_dataset_csv_path


class Evaluator:
    GEN_ANALYSIS_PROCESSED_FNAME = "llm_analysis_processed.pkl"
    MATCHED_ANNOTATIONS_FNAME = "matched_annotations.pkl"
    MATCH_METRICS_FNAME = "match_metrics.json"

    def __init__(
        self,
        submission: DatasetSubmission,
        text_gen: TextGenerator,
        use_code_cache: bool = True,
        output_dir: str = ".",
    ):
        self.llm_history = LLMHistory()
        self.submission = submission
        self.use_code_cache = use_code_cache
        self.output_dir = output_dir

        self.convert = Convert(
            submission.dataset_name,
            text_gen=text_gen,
            llm_history=self.llm_history,
            use_code_cache=use_code_cache,
            output_dir=output_dir,
        )
        self.matcher: SubmissionMatch = SubmissionMatch(
            submission.dataset_name,
            text_gen=text_gen,
            llm_history=self.llm_history,
        )
        self.transform_run_result: EvalRunResults = None

    async def get_run_results(
        self, res_type: RunResultModes, info: str, is_error=True, eval_res=None
    ):
        if is_error:
            logger.error(info)
        else:
            logger.info(info)

        await self.convert.transform_executor.nb_executor.terminate()
        await self.convert.code_executor.nb_executor.terminate()
        if self.convert.annotation.nb_executor is not None:
            await self.convert.annotation.nb_executor.nb_executor.terminate()

        return EvalRunResults(
            res_type=res_type,
            res_type_transform=(
                self.transform_run_result.res_type
                if self.transform_run_result is not None
                else None
            ),
            info=info,
            eval_lm_history=self.llm_history,
            eval_metrics=eval_res,
        )

    async def process_analysis(
        self, analysis: EntireAnalysis
    ) -> Union[EntireAnalysisProcessed, EvalRunResults]:
        try:
            analysis_processed, eval_result = (
                await self.convert.convert_entire_analysis(analysis)
            )
            if eval_result is not None:
                logger.error(eval_result.info)
                logger.info("Continuing with the next step, skipping transformations.")
                self.transform_run_result = eval_result
        except Exception as e:
            raise LMSubmissionConversionError(
                f"Failed to convert submission: {traceback.format_exc()}"
            )
        return analysis_processed

    async def load_ground_truth(self) -> Union[AnnotationDBData, EvalRunResults]:
        try:
            gnd_truth = load_ground_truth_data(
                self.submission.dataset_name, self.output_dir
            )
        except Exception as e:
            raise LoadGroundTruthError(
                f"Failed to load ground truth: {traceback.format_exc()}"
            )
        return gnd_truth

    async def match_annotations(
        self, gnd_truth: AnnotationDBData, analysis_processed: EntireAnalysisProcessed
    ):
        try:
            matched_annotations: MatchedAnnotations = await self.matcher.match_all(
                gnd_truth, analysis_processed
            )
        except Exception as e:
            raise MatchAnnotationsError(
                f"Failed to match submission: {traceback.format_exc()}"
            )
        return matched_annotations

    async def get_metrics(self, matched_annotations: MatchedAnnotations):
        try:
            match_metrics = get_metrics_from_match_obj(matched_annotations)
        except Exception as e:
            raise GetMetricsError(
                f"Failed to get match metrics: {traceback.format_exc()}"
            )
        return match_metrics

    async def run_eval(self, analysis: EntireAnalysis) -> EvalResult:
        analysis_processed = None
        matched_annotations = None
        match_metrics = None
        try:
            analysis_processed = await self.process_analysis(analysis)
            gnd_truth = await self.load_ground_truth()
            matched_annotations = await self.match_annotations(
                gnd_truth, analysis_processed
            )
            logger.success(f"Got matched annotations")
            match_metrics = await self.get_metrics(matched_annotations)
            run_results = await self.get_run_results(
                RunResultModes.FINISHED_SUCCESSFULLY,
                "Successfully ran evaluation",
                is_error=False,
            )
        except RunError as e:
            run_results = await self.get_run_results(
                e.res_type, e.message, is_error=True
            )
        return EvalResult(
            dataset_name=self.submission.dataset_name,
            analysis=analysis,
            analysis_processed=analysis_processed,
            matched_annotations=matched_annotations,
            metrics=match_metrics,
            eval_run_result=run_results,
        )
