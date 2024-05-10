from datasets import Dataset, DatasetDict, load_dataset
from huggingface_hub import HfApi, HfFolder

# Load parquet files without predefined splits
train_dataset = load_dataset('parquet', data_files='train-pairwise_preferences.parquet')['train']
test_dataset = load_dataset('parquet', data_files='test-pairwise_preferences.parquet')['train']
validation_dataset = load_dataset('parquet', data_files='validation-pairwise_preferences.parquet')['train']

# Assign splits manually
dataset_dict = DatasetDict({
    'train': train_dataset,
    'test': test_dataset,
    'validation': validation_dataset
})

# Authentication with Hugging Face Hub
# Ensure you are logged in to Huggingface, either using `huggingface-cli login` or by setting the token in the script
api = HfApi()
token = HfFolder.get_token()
username = api.whoami(token)['name']

# Choose a name for your dataset
dataset_name = "pairwise_preferences"
dataset_repo_name = f"{username}/{dataset_name}"

# Push the dataset to the Hugging Face Hub
dataset_dict.push_to_hub(dataset_repo_name)
