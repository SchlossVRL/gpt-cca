import pandas as pd
import matplotlib.pyplot as plt

def load_responses_df():
    # Load the CSV file, selecting only relevant columns and skipping the first unnamed column
    all_stim_df = pd.read_csv(
        "../../data/all_stim.csv",
        usecols=['concept', 'color_index', 'response']
    )

    # Ensure 'color_index' is of integer type
    all_stim_df['color_index'] = all_stim_df['color_index'].astype(int)

    # Convert 'response' to numeric, coercing errors to NaN
    all_stim_df['response'] = pd.to_numeric(all_stim_df['response'], errors='coerce')

    # Pivot the DataFrame: concepts as rows, color_index as columns, response as values
    pivoted_df = all_stim_df.pivot(index='concept', columns='color_index', values='response')

    # Sort the columns numerically from 0 to 69
    pivoted_df = pivoted_df.sort_index(axis=1)
    
    pivoted_df.to_csv(f'../../data/gpt4o-11052024_0_images.csv')

    return pivoted_df

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
    # Initialize an empty dictionary to store correlations
    correlations = {}
    
    # Iterate through each concept in the DataFrame
    for concept, row in df.iterrows():
        if concept in benchmark_data.index:
            benchmark_row = benchmark_data.loc[concept]
            # Compute the Pearson correlation
            corr = row.corr(benchmark_row)
            correlations[concept] = corr
    
    # Convert the dictionary to a DataFrame with a 'Correlation' column
    correlation_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['Correlation'])
    
    return correlation_df

if __name__ == "__main__":
    # Load benchmark and response data
    benchmark_data = load_benchmark_data()
    responses_df = load_responses_df()
    
    # Compute correlations
    correlations = compute_correlation(responses_df, benchmark_data)
    
    # Calculate the average correlation
    average_correlation = correlations['Correlation'].mean()
    
    # Reset index to use 'concept' as a column for plotting
    correlations_reset = correlations.reset_index().rename(columns={'index': 'Concept'})
    
    # Plot the data
    plt.figure(figsize=(12, 8))
    plt.scatter(correlations_reset['Concept'], correlations_reset['Correlation'])
    plt.title('GPT vs Human Correlation')
    plt.xlabel('Concepts')
    plt.ylabel('Correlation')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.axhline(y=average_correlation, color='r', label=f'Average Correlation: {average_correlation:.3f}')
    plt.legend()
    plt.tight_layout()
    plt.show()