import matplotlib.pyplot as plt
from PIL import Image, UnidentifiedImageError
import io
import pandas as pd
from datasets import load_dataset
from tqdm import tqdm
import base64

def image_to_base64(img):
    """Converts a PIL image to a base64-encoded string."""
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")  # Save image to buffer
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Load the dataset
dataset = load_dataset("THUDM/ImageRewardDB", "1k", split='train', trust_remote_code=True)
data = dataset.se

# Initializing variables for processing
pairwise_preferences = []
current_prompt = None
current_group = []

from tqdm import tqdm

data_length = len(data)
index = 0

with tqdm(total=data_length, desc="Processing Images", position=0, leave=True) as pbar:
    while index < data_length:
        try:
            entry = data[index]
            if entry['prompt'] != current_prompt:
                # Process the current group
                if current_group:
                    for i in range(len(current_group)):
                        for j in range(i + 1, len(current_group)):
                            if current_group[i]['rank'] != current_group[j]['rank']:
                                winner = image_to_base64(current_group[i]['image'])
                                loser = image_to_base64(current_group[j]['image'])
                                pairwise_preferences.append({
                                    'caption': current_prompt,
                                    'jpg_0': winner,
                                    'jpg_1': loser,
                                    'label_0': 1,
                                    'label_1': 0
                                })
                # Reset for new prompt
                current_prompt = entry['prompt']
                current_group = []

            current_group.append(entry)
        except UnidentifiedImageError:
            print("Could not read image. Skipping...")
            index += 1
            pbar.update(1)
            continue
        except Exception as e:
            print(f"An error occurred: {e}")
            index += 1
            pbar.update(1)
            continue

        index += 1
        pbar.update(1)

# Don't forget to process the last group if exists
if current_group:
    for i in range(len(current_group)):
        for j in range(i + 1, len(current_group)):
            if current_group[i]['rank'] != current_group[j]['rank']:
                winner = image_to_base64(current_group[i]['image'])
                loser = image_to_base64(current_group[j]['image'])
                pairwise_preferences.append({
                    'caption': current_prompt,
                    'jpg_0': winner,
                    'jpg_1': loser,
                    'label_0': 1,
                    'label_1': 0
                })

# Convert the list to DataFrame
pairwise_df = pd.DataFrame(pairwise_preferences)

# Save the DataFrame to a Parquet file
pairwise_df.to_parquet('pairwise_preferences.parquet')

# Output message confirming the process is completed
print("Dataset has been processed and saved to 'pairwise_preferences.parquet'.")
