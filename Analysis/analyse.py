import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
azure_data = pd.read_csv('azure_avg.csv')
gcloud_data = pd.read_csv('gcloud_avg.csv')
local_data = pd.read_csv('local_avg.csv')

# Comparison for a specific query (e.g., Query1)
query = 'Query1'

# Extract data for the selected query from each dataset
azure_query_data = azure_data[azure_data['Query'] == query].drop('Query', axis=1).T
gcloud_query_data = gcloud_data[gcloud_data['Query'] == query].drop('Query', axis=1).T
local_query_data = local_data[local_data['Query'] == query].drop('Query', axis=1).T

# Rename columns for clarity in the graph
azure_query_data.columns = ['Azure']
gcloud_query_data.columns = ['GCloud']
local_query_data.columns = ['Local']

# Combine data for plotting
combined_data = pd.concat([azure_query_data, gcloud_query_data, local_query_data], axis=1)

# Plotting the combined graph
plt.figure(figsize=(10, 6))
combined_data.plot(kind='bar', ax=plt.gca())
plt.title(f'Performance Comparison for {query}')
plt.ylabel('Average Time (seconds)')
plt.xlabel('Scale Factor')
scale_factor_labels = ['1', '10', '100', '1000']
plt.xticks(ticks=range(len(scale_factor_labels)), labels=scale_factor_labels, rotation=0)
plt.yscale('log')  # Using logarithmic scale due to large differences in values
plt.grid(True)
plt.legend()
plt.savefig('comparison_local.png')

# Comparison graphs for Azure and GCloud
azure_comparison_data = azure_data.set_index('Query')
gcloud_comparison_data = gcloud_data.set_index('Query')

# Create figure and axes for subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
fig.suptitle('Performance Comparison Across Queries for Azure and GCloud')

# List of scale factors
scale_factors = ['1', '10', '100', '1000']

# Plotting comparison for each scale factor
for i, scale in enumerate(scale_factors):
    ax = axes[i//2, i%2]
    azure_comparison_data[f'Average Time (seconds)_{scale}'].plot(kind='bar', ax=ax, color='blue', position=0, width=0.4, label='Azure')
    gcloud_comparison_data[f'Average Time (seconds)_{scale}'].plot(kind='bar', ax=ax, color='green', position=1, width=0.4, label='GCloud')
    ax.set_title(f'Scale Factor {scale}')
    ax.set_ylabel('Average Time (seconds)')
    ax.set_xlabel('Query')
    ax.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('g_cloud_vs_azure.png')