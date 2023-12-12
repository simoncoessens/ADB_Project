import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
azure_data = pd.read_csv('azure_avg.csv')
gcloud_data = pd.read_csv('gcloud_avg.csv')
local_data = pd.read_csv('local_avg.csv')

# Combining all average times into a single DataFrame for box plot
all_averages = pd.DataFrame({
    'Azure': azure_data.drop('Query', axis=1).values.flatten(),
    'GCloud': gcloud_data.drop('Query', axis=1).values.flatten(),
    'Local': local_data.drop('Query', axis=1).values.flatten()
})

# Creating the box plot
plt.figure(figsize=(10, 6))
all_averages.boxplot()
plt.title('Box Plot of Average Times Across Platforms')
plt.ylabel('Average Time (seconds)')
plt.yscale('log')  # Using logarithmic scale due to large differences in values
plt.grid(True)

# Display the plot
plt.savefig('box_plot_comparison.png')

