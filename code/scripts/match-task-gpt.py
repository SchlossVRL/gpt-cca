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

csv_exists = False

if csv_exists==True:
    # If there is a csv file already, read it in
    output_df = pd.read_csv(f'../../data/match_task_output.csv')
if csv_exists==False:
    # If there is no csv file, create it
    input_df = pd.read_csv(f'../../data/match_task_input.csv')
    output_df = input_df.copy()
    output_df['response'] = np.nan
    output_df['img_url'] = input_df['fname'].apply(lambda x: f"data:image/jpeg;base64,{base64.b64encode(open(f'../../data/match_task_images/{x}', 'rb').read()).decode('utf-8')}")
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
        max_tokens=100,
        temperature=0
        )
    return response.choices[0].message.content
    
#### apply return_chat_response to every row in new_df_sub with a progress bar in terminal and save out the results to a csv file every 100 rows
if csv_exists==True:
    responses = output_df[~output_df.response.isnull()]['response'].to_list()
if csv_exists==False:
    responses = []
    
for i, row in tqdm.tqdm(output_df.iterrows(), total=len(output_df)):
    if isinstance(row.response, str):
        continue
    # get the response from the api for each row
    ##hardcode a system prompt
    system_prompt = "You are a helpful assistant who is an expert on color semantics -- how colors relate to concepts."
    response = return_chat_response(system_prompt, row['prompt'], row['img_url'])
    responses.append(response)
    # Save the responses to the csv file every 100 rows
    if i % 10 == 0:
        if len(responses) < len(output_df):
            tmp_responses = responses + [None] * (len(output_df) - len(responses))
        output_df['response'] = tmp_responses
        output_df.to_csv(f'../../data/match_task_output.csv')
output_df['response'] = responses

output_df.to_csv(f'../../data/match_task_output.csv')