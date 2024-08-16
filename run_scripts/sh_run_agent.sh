#!/bin/bash

# Make sure the provider and model are correctly used 
# Array of llm values
llm_values=("anthropic:claude-3.5-sonnet")
# Array of run_dataset values
run_datasets=("affairs" "hurricane" "amtl" "boxes" "caschools" "crofoot" "fish" "mortgage" "panda_nuts" "reading" "soccer" "teachingratings")
set -e  # Exit immediately if a command exits with a non-zero status
trap 'echo "Script failed at: $(eval echo $BASH_COMMAND)"' ERR


for model_provider in "${llm_values[@]}"; do
    IFS=':' read -r provider llm  <<< "$model_provider"
    for run_dataset in "${run_datasets[@]}"; do
        output_folder="./outputs/final/${llm}_agent/${run_dataset}"
        echo "running with llm=$llm, provider=$provider, run_dataset=$run_dataset"

        # Execute the python script with the current values
        python run_gen_analyses.py --llm_provider $provider \
            --llm_model $llm \
            --output_dir $output_folder \
            --run_dataset $run_dataset\
            --use_agent \
            -n 20
    done
done