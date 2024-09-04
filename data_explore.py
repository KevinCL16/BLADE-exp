from blade_bench.data import load_dataset_info, list_datasets, DatasetInfo, load_ground_truth, AnnotationDBData
from blade_bench.llms import llm

all_datasets = list_datasets()
dinfo: DatasetInfo = load_dataset_info("fish", load_df=True)
rq = dinfo.research_question
df = dinfo.df
print("***********Research Question****************\n" + rq + "\n")
# each dataset annotations will be prepared when it is run the first time
gnd_truth: AnnotationDBData = load_ground_truth('fish')
print((gnd_truth.transform_specs))
print((gnd_truth.cv_specs))

'''gen = llm(provider="OpenAI", model="gpt-4o")
response = gen.generate([{"role": "user", "content": "Who are you?"}])
print(response)'''