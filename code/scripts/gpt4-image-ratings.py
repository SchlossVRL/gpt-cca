import os
import openai
import pandas as pd
import numpy as np
import base64
import requests
from openai import OpenAI


# OpenAI API Key|| Make sure to place the SVRL_api_key.txt file in the same directory as this script
with open('SVRL_api_key.txt') as f:
    openai.api_key = f.readline()
    f.close()

client = OpenAI(api_key=openai.api_key)

# load the ratings data from text only prompts
script_dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(
    script_dir, '../../data/gpt4_ratings_anchored_final.csv'))
# rename unnamed column to concept
df.rename(columns={'Unnamed: 0': 'concept'}, inplace=True)
# get the unique concept names
concepts = df['concept'].unique()
color_image_paths = [os.path.join(script_dir, '../../images', x) for x in os.listdir(os.path.join(script_dir, '../../images')) if x.endswith('.png')]

# Sort the list numerically based on the number in the filename
color_image_paths = sorted(color_image_paths, key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))

# Load the UW71coordinateslong.csv file
uw71_file_path = os.path.join(script_dir, '../../data/UW71coordinates_long.csv')
uw71_df = pd.read_csv(uw71_file_path)

# Create a dictionary to map color index to hex code
color_index_to_hex = dict(zip(uw71_df['color_index'], uw71_df['color_hex']))

# Create the hashmap where the color file is the key and the hex code is the value
color_file_to_hex = {}
for color_image_path in color_image_paths:
    # Extract the color index from the filename
    color_index = int(os.path.splitext(os.path.basename(color_image_path))[0])
    # Get the corresponding hex code
    hex_code = color_index_to_hex.get(color_index)
    # Add to the hashmap
    color_file_to_hex[color_image_path] = hex_code

# print(color_file_to_hex)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to create the batch file with the prompts
def create_batch_file(batch_file, concepts, color_image_paths):
    with open(batch_file, 'w') as f:
        for concept in concepts:
            for color_image_path in color_image_paths:
                base64_image = encode_image(color_image_path)
                # f.write(
                #     f'''{{"custom_id": "{concept}-{os.path.basename(color_image_path)}", "method": "POST", "url": "/v1/chat/completions", "body": {{ "model": "gpt-4o-mini", "messages": [ {{ "role": "system", "content": "You are an expert on color-concept associations." }}, {{ "role": "user", "content": "I will give you the hexcode for a color and a concept. Rate on a continuous scale from 0 to 1, using 3 decimal places, how associated the color is with the concept. The concept is '{concept}'. Color: {color_file_to_hex[color_image_path]}. Answer with only the number." }}], "temperature" : 0 }}}}\n'''
                #   )
                f.write(f'{{"custom_id": "{concept}-{os.path.basename(color_image_path)}", "method": "POST", "url": "/v1/chat/completions", "body": {{"model": "gpt-4o-mini", "messages": [{{"role": "user", "content": [{{"type": "text", "text": "Rate on a continuous scale from 0 to 1, using 3 decimal places, how associated the colored patch in the image is with the concept \'{concept}\'. Answer with only the number."}}, {{"type": "image_url", "image_url": {{"url": "data:image/jpeg;base64,{base64_image}"}}}}]}}], "temperature": 1}}}}\n')

    f.close()

# Retrieve the batch file path
batch_file = os.path.join(script_dir, 'batch_inputs.jsonl')

create_batch_file(batch_file, concepts, color_image_paths)

# Create the batch input file
# batch_input_file = client.files.create(
#     file=open(batch_file, 'rb'),
#     purpose='batch'
# )

# # Create the batch job
# batch_job = client.batches.create(
#   input_file_id=batch_input_file.id,
#   endpoint="/v1/chat/completions",
#   completion_window="24h",
# )

# # Retrieve the batch id for the job
# batch_input_file_id = client.batches.retrieve(batch_job.id)

# print(batch_input_file_id)


### prompt structure: imagine cycling through all the concepts for each concept cycling through all color images

# [{
#         "role": "system",
#         "content": "You are an expert on color-concept associations."
#     },

#     {
#         "role": "user",
#         "content": f"Rate on a continuous scale from 0 to 1, using 3 decimal places, how associated the colored patch in the image is with the concept {this_concept}.\
# Answer with only the number:"
#     }],



#### example code from OpenAI API documentation on how to use image API

# # Function to encode the image
# def encode_image(image_path):
#   with open(image_path, "rb") as image_file:
#     return base64.b64encode(image_file.read()).decode('utf-8')

# # Path to your image
# image_path = "path_to_your_image.jpg"

# # Getting the base64 string
# base64_image = encode_image(image_path)

# headers = {
#   "Content-Type": "application/json",
#   "Authorization": f"Bearer {api_key}"
# }

# payload = {
#   "model": "gpt-4o-mini",
#   "messages": [
#     {
#       "role": "user",
#       "content": [
#         {
#           "type": "text",
#           "text": "What’s in this image?"
#         },
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": f"data:image/jpeg;base64,{base64_image}"
#           }
#         }
#       ]
#     }
#   ],
#   "max_tokens": 30
# }

# response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
