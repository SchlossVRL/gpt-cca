import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Function to load data from a CSV file and convert it to a DataFrame.
"""
def load_data(path):
    # Load the CSV file from the path, setting the 'concept' column as the index
    df = pd.read_csv(path, header=0, index_col=0)
    
    # Convert all data to numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Filter out columns that cannot be converted to integers
    numeric_columns = [col for col in df.columns if col.isdigit()]
    df = df[numeric_columns]
    
    # convert the column type to int for sorting 
    df.columns = df.columns.astype(int)
    # sort the columns
    df = df.sort_index(axis=1)
    return df

def show_plot():
    num_categories = len(categories)
    fig, axes = plt.subplots(nrows=2, ncols=(num_categories + 1) // 2, figsize=(15, 10), constrained_layout=True)
    axes = axes.flatten()

    # Plot each category in a separate subplot
    for idx, (category, concepts) in enumerate(categories.items()):
        # if the concept is in the category, then add it to the list of concepts
        category_df = avg_df[avg_df['Concept'].isin(concepts)]
        x = np.arange(len(category_df))  # label locations
        width = 0.25  # width for each of the three bars

        # Plot bars for each concept in the category
        axes[idx].bar(x - width, category_df['4o Avg'], width, label='4o')
        axes[idx].bar(x, category_df['Benchmark Avg'], width, label='Benchmark')
        axes[idx].bar(x + width, category_df['4o-mini Avg'], width, label='4o-mini')

        # Set labels and title
        axes[idx].set_title(category)
        axes[idx].set_xticks(x)
        axes[idx].set_xticklabels(category_df['Concept'], rotation=90)
        axes[idx].set_ylim(0, 1)

    # legend
    fig.legend(['GPT 4o', 'Benchmark', 'GPT 4o-mini'], loc='upper right')
    # show the plot
    plt.show()

if __name__ == "__main__":
    # Load benchmark and data from GPT-4o and GPT-4o-mini
    benchmark_data = load_data('../../data/gpt4_ratings.csv')
    responses_4o_df = load_data("../../data/gpt-4o-11052024_0_images.csv")
    responses_4o_mini_df = load_data("../../data/gpt-4o-mini-11052024_0_images.csv")

    # Align all DataFrames to have the same index
    common_index = benchmark_data.index.intersection(responses_4o_df.index).intersection(responses_4o_mini_df.index)
    benchmark_data = benchmark_data.reindex(common_index)
    responses_4o_df = responses_4o_df.reindex(common_index)
    responses_4o_mini_df = responses_4o_mini_df.reindex(common_index)

    # Calculate average for each concept
    responses_4o_df['average'] = responses_4o_df.mean(axis=1)
    benchmark_data['average'] = benchmark_data.mean(axis=1)
    responses_4o_mini_df['average'] = responses_4o_mini_df.mean(axis=1)
    
    # Create a new DataFrame with 'Concept', '4o Avg', 'Benchmark Avg', and '4o-mini Avg'
    avg_df = pd.DataFrame({
        'Concept': responses_4o_df.index,
        '4o Avg': responses_4o_df['average'],
        'Benchmark Avg': benchmark_data['average'],
        '4o-mini Avg': responses_4o_mini_df['average']
    })

    # define categories and the concepts in each category (from https://arxiv.org/pdf/2406.17781)
    categories = {
        "animals": ["lion", "frog", "bear", "bird", "fish"],
        "clothes": ["socks", "pants", "shoes", "shirt", "dress"],
        "fruits": ["watermelon", "blueberry", "lemon", "mango", "strawberry"],
        "fruits_2": ["banana", "grape", "apple", "peach", "cherry"],
        "scenes": ["ocean", "sky", "field", "beach", "sunset"],
        "vegetables": ["celery", "carrot", "corn", "eggplant", "mushroom"],
        "vehicles": ["boat", "plane", "truck", "car", "train"],
        "activities": ["sleeping", "eating", "working", "driving", "leisure"],
        "directions": ["above", "below", "far", "near", "beside"],
        "emotions": ["happy", "sad", "angry", "disgust", "fearful"],
        "properties": ["speed", "comfort", "efficiency", "safety", "reliability"],
        "values": ["love", "evil", "greed", "peace", "justice"],
        "times-of-day": ["night", "day", "noon", "dusk", "dawn"],
        "weather": ["sandstorm", "blizzard", "drought", "hurricane", "lightning"]
    }

    # Show the plot
    show_plot()