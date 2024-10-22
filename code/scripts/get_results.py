import json
import openai
from openai import OpenAI
import pandas as pd

def convert_df_to_csv(df):
    # Save the DataFrame to a CSV file
    file = open("file_name", "w")
    file.write(df.to_csv())

def create_df(result):
    # Load data from the result to a new dictionary
    data = {}
    for line in result.decode('utf-8').split('\n'):
        if line:
            entry = json.loads(line)
            # Separate into the custom_id and response
            custom_id = entry['custom_id']
            response = entry['response']['body']['choices'][0]['message']['content']
            
            # Separate custom id into concept and index
            concept = custom_id.split('-')[0]
            index = int(custom_id.split('-')[1].split('.')[0])
            
            # Initialize concept in the data dictionary if not already present
            if concept not in data:
                data[concept] = {}
            
            # Store the response value as a float at the respective index
            data[concept][index] = float(response)
    
    # Convert the dictionary to a DataFrame, filling missing values with NaN
    df = pd.DataFrame.from_dict(data, orient='index').sort_index(axis=1)
    return df

def load_benchmark_data():
    # Load the CSV file, setting the 'concept' column as the index
    df = pd.read_csv('../../data/gpt4_ratings.csv', header=0, index_col=0)
    df = df.apply(pd.to_numeric, errors='coerce')

    # convert the column type to int for sorting 
    df.columns = df.columns.astype(int)
    # sort the columns
    df = df.sort_index(axis=1)
    return df

def compute_correlation(df, benchmark_data):
    correlation = []
    # iterate through the rows of df and benchmark_data at the same time 
    for concept, row in df.iterrows():
        benchmark_row = benchmark_data.loc[concept]
        # compute the pearson correlation between the two rows
        corr = row.corr(benchmark_row)
        correlation.append(corr)
    return correlation

if __name__ == "__main__":
    with open('SVRL_api_key.txt') as f:
        openai.api_key = f.readline().strip()

    client = OpenAI(api_key=openai.api_key)

    # Get the most recent batch job and print the results
    batch_job_id = client.batches.list().data[0].id
    
    print(client.batches.list().data[0])
    # for batch in client.batches.list().data:
    #     print(batch.status)

    # Retrieve the batch job status
    batch_job = client.batches.retrieve(batch_job_id)
    
    # Uncomment the following line to cancel the batch job
    # client.batches.cancel("batch_671718cb6c10819093c05c8b42236598")
    
    # Uncomment the following lines to save the results to a file
    # result_file_name = "results.jsonl"
    # with open(result_file_name, 'rb') as file:
    #     result_content = file.read()
    # df = create_df(result_content)
    # convert_df_to_csv(df)

    # Check if the job has completed
    if batch_job.status == "completed":
        result_file_id = batch_job.output_file_id

        # Retrieve the content of the result file
        result = client.files.content(result_file_id).content
        
        result_file_name = "results.jsonl"
        with open(result_file_name, 'wb') as file:
            file.write(result)

        # Create and print the DataFrame
        df = create_df(result)
        benchmark_data = load_benchmark_data()
        
        # print the correlation for every concept
        correlation = compute_correlation(df, benchmark_data)
        for concept in df.index:
            print(f"{concept}: {correlation[df.index.get_loc(concept)]}")
            
        # print(f"Correlation: {sum(correlation) / len(correlation)}")
        # print average correlation excluding the NaN values
        sum=0
        count=0
        for x in correlation:
            if not pd.isna(x):
                sum+=x
                count+=1
        print("Average correlation: ", sum/count)

        print(f"Results saved to results.jsonl")
        
        # with(open("correlation.txt", "w")) as f:
        #     f.write(f"Correlation: {sum(correlation) / len(correlation)}")
    else:
        print(f"Current status: {batch_job.status}")