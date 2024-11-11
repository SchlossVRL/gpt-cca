import numpy as np
import pandas as pd
import tqdm
import re
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
import openai
from openai import OpenAI
import os
import base64

def create_df(concepts, color_image_paths):
    # gather all the concepts
    all_concepts = [concept for concept in concepts for color_image_path in color_image_paths]
    # store the color index for each concept
    all_color_index = [i for _ in range(len(concepts)) for i in range(0, 71)]
    # store the system prompts for each concept
    all_system_prompts = ["You are an expert on color-concept associations." for concept in concepts for i in range (1, 72)]
    # store the user prompts for each concept 
    all_user_prompts = [f"Rate on a continuous scale from 0 to 1, using 3 decimal places, how associated the colored patch in the image is with the concept '{concept}'. Answer with only the number." for concept in concepts for i in range (1, 72)]

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    # encode the images
    encoded_images = [f"data:image/jpeg;base64,{encode_image(color_image_path)}" for color_image_path in color_image_paths]
    # store the image urls for each concept
    all_img_urls = encoded_images * len(concepts)

    # create the dataframe with the columns concept, color_index, system_prompt, user_prompt, img_url, response
    all_stim_df = pd.DataFrame({'concept': all_concepts, 'color_index': all_color_index, 'system_prompt': all_system_prompts, 'user_prompt': all_user_prompts, 'img_url': all_img_urls, 'response': None})
    return all_stim_df

def load_concepts_and_colors():
    # load the ratings data from text only prompts
    script_dir = os.path.dirname(__file__)
    # read the csv file
    df = pd.read_csv(os.path.join(
        script_dir, '../../data/gpt4_ratings_anchored_final.csv'))
    # rename unnamed column to concept
    df.rename(columns={'Unnamed: 0': 'concept'}, inplace=True)
    # get the unique concept names
    concepts = df['concept'].unique()
    # get the color image paths
    color_image_paths = [os.path.join(script_dir, '../../images', x) for x in os.listdir(os.path.join(script_dir, '../../images')) if x.endswith('.png')]

    # Sort the list numerically based on the number in the filename
    color_image_paths = sorted(color_image_paths, key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
    # create the dataframe and return it 
    return create_df(concepts, color_image_paths)

### make these into flags eventually
smart_icl = False
csv_exists = False

if smart_icl==True:
    out_fname = 'semantic_norms_gpt4o_human_trials_6_shot_smart.csv'
elif smart_icl==False:
    out_fname = 'semantic_norms_gpt4o_human_trials_6_shot_naive.csv'

if csv_exists==True:
    # If there is a csv file already, read it in
    all_stim_df = pd.read_csv(f'../../data/all_stim.csv', index_col=0)
if csv_exists==False:
    # If there is no csv file, create it
    all_stim_df = load_concepts_and_colors()
    all_stim_df.to_csv(f'../../data/all_stim.csv')
    
# load the api key
with open('SVRL_api_key.txt') as f:
    openai.api_key = f.readline()
    f.close()
client = OpenAI(api_key=openai.api_key)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def return_chat_response(system_prompt, user_prompt, image_url):
    # make the request to the api
    response = completion_with_backoff(model="gpt-4o", messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ],
        },
        ],
        # Set to 5 because the number from 0.000 to 1.000 won't exceed 5 tokens
        # Can also change to 10 tokens or completely get rid of it if needed
        max_tokens=5,
        temperature=0
        )
    return response.choices[0].message.content
    
#### apply return_chat_response to every row in new_df_sub with a progress bar in terminal and save out the results to a csv file every 100 rows
if csv_exists==True:
    responses = all_stim_df[~all_stim_df.response.isnull()]['response'].to_list()
if csv_exists==False:
    responses = []
    
for i, row in tqdm.tqdm(all_stim_df.iterrows(), total=len(all_stim_df)):
    if isinstance(row.response, str):
        continue
    # get the response from the api for each row
    response = return_chat_response(row['system_prompt'], row['user_prompt'], row['img_url'])
    responses.append(response)
    # Save the responses to the csv file every 100 rows
    if i % 100 == 0:
        if len(responses) < len(all_stim_df):
            tmp_responses = responses + [None] * (len(all_stim_df) - len(responses))
        all_stim_df['response'] = tmp_responses
        all_stim_df.to_csv(f'../../data/all_stim.csv')
all_stim_df['response'] = responses

all_stim_df.to_csv(f'../../data/all_stim.csv')