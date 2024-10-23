import pandas as pd
import matplotlib.pyplot as plt

# Read file
with open('correlation/gpt-4o-mini_images_1_run2.txt') as f:
    data = f.read()

# Parse data for df
lines = data.splitlines()
parsed_data = [line.split(': ') for line in lines]

# Create df and load values
df = pd.DataFrame(parsed_data, columns=['Concept', 'Correlation'])
df['Correlation'] = pd.to_numeric(df['Correlation'])
# Average correlation
average_correlation = df['Correlation'].mean()

# Plot the data
plt.figure(figsize=(12, 8))
plt.scatter(df['Concept'], df['Correlation'])
plt.title('GPT vs Human Correlation')
plt.xlabel('Concepts')
plt.ylabel('Correlation')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.axhline(y=average_correlation, color='r')
plt.tight_layout()
plt.show()