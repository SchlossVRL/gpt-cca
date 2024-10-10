import os
import openai
import pandas as pd
import numpy as np
import base64


# OpenAI API Key|| Make sure to place the SVRL_api_key.txt file in the same directory as this script    
with open('SVRL_api_key.txt') as f:
    openai.api_key= f.readline()
    f.close()

### load the ratings data from text only prompts
script_dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(script_dir, '../../data/gpt4_ratings_anchored_final.csv'))
### rename unnamed column to concept
df.rename(columns={'Unnamed: 0':'concept'}, inplace=True)
### get the unique concept names
concepts = df['concept'].unique()
color_image_paths = [os.path.join(script_dir, '../../images',x) for x in os.listdir(os.path.join(script_dir, '../../images')) if x.endswith('.png')]


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
