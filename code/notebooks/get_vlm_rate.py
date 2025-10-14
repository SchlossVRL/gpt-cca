import base64
import pandas as pd
import numpy as np
from openai import OpenAI

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def make_ratings_mat(grouped_ratings_df):
    
    mat = np.zeros((len(np.unique(grouped_ratings_df.prompt)),71))
    for i,con in enumerate(np.unique(grouped_ratings_df.prompt)):
        ds = grouped_ratings_df[grouped_ratings_df.prompt==con]
        mat[i,:] = ds.iloc[:,3].values


    mat = pd.DataFrame(mat, index =np.unique(grouped_ratings_df.prompt), columns = np.arange(mat.shape[1]) )
    cmeans = mat.mean().values
    return mat, cmeans

set_1_raw = pd.read_csv('../../data/uw71_set1_redo_raw.csv')
set_2_raw = pd.read_csv('../../data/uw71_set2_raw.csv')
set_3_raw = pd.read_csv('../../data/uw71_set3_raw.csv')
set1_grouped = set_1_raw.groupby(['concept','prompt','color_index']).response.agg(mean_rating = 'mean', se ='sem').reset_index()
set2_grouped = set_2_raw.groupby(['concept','prompt','color_index']).response.agg(mean_rating = 'mean', se ='sem').reset_index()
set3_grouped = set_3_raw.groupby(['concept','prompt','color_index']).response.agg(mean_rating = 'mean', se ='sem').reset_index()

ratings1,ratings_cmeans1= make_ratings_mat(set1_grouped)
ratings2,ratings_cmeans2= make_ratings_mat(set2_grouped)
ratings3,ratings_cmeans3= make_ratings_mat(set3_grouped)

concept_list = set1_grouped.pivot(index=['prompt','concept'], columns='color_index', values='mean_rating').reset_index().sort_values(by=['concept','prompt']).reset_index(drop=True)['prompt'].values
concept_list.sort()
concept_order  = {concept: i for i, concept in enumerate(concept_list)}

### vertically stack the ratings matrices
ratings_all = pd.concat([ratings1,ratings2,ratings3])


uw71coords = pd.read_csv('../../data/UW71coordinates_long.csv')

client = OpenAI(api_key ="" )

import time
from tqdm import tqdm
from IPython.display import clear_output
completed_concepts = ['above','angry','beach']
assocs = np.zeros((70,71), dtype = object)
for i,this_concept in enumerate(ratings_all.index.values):
  if this_concept in completed_concepts:
    continue
  
  clear_output()
  print(f'Evaluating:{this_concept}')

  for j,this_color in enumerate(tqdm(uw71coords.color_hex.values)):

    time.sleep(2)

    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
    {
            "role": "system",
            "content": "You are an expert on color-concept associations."
          },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": f"I will show you an image of a color patch. Rate on a continuous scale from 0 to 1, using 3 decimal places, how associated the color patch is with the concept '{this_concept}'.\
            Okay, now let's do the rating task. No matter what, always answer with only the number:"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encode_image(f'../../plots/patches/{this_color}.png')}"
          },
        },
      ],
    }
  ],
  max_tokens=10,
  temperature=0,
)
    
    assocs[i,j] = (response.choices[0].message.content)
  gptv_assoc_df = pd.DataFrame(assocs, index = ratings_all.index.values, columns = np.arange(71))
  gptv_assoc_df.to_csv('../../data/gpt4v_ratings_no_anchor.csv')
