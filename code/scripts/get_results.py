import json
import openai
from openai import OpenAI

with open('SVRL_api_key.txt') as f:
    openai.api_key = f.readline()
    f.close()

client = OpenAI(api_key=openai.api_key)

# get the most recent batch job and print the results
print(client.batches.list().data[0])

# save the batch id of the most recent batch job
batch_job_id = client.batches.list().data[0].id

# Retrieve the batch job status
batch_job = client.batches.retrieve(batch_job_id)

# Check if the job has completed
if batch_job.status == "completed":
    result_file_id = batch_job.output_file_id

    # Retrieve the content of the result file
    result = client.files.content(result_file_id).content

    # Save the results to a file
    result_file_name = "results.jsonl"
    with open(result_file_name, 'wb') as file:
        file.write(result)

    print(f"Results saved to results.jsonl")
else:
    print(f"Current status: {batch_job.status}")
