import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data from the tables
data_google_cloud = {
    "Operation": ["create_database", "users", "vehicles", "drivers", "payments", "rides"],
    "Scale 1 (s)": [0.51, 0.24, 0.26, 0.24, 0.26, 24.99],
    "Scale 10 (s)": [0.21, 0.24, 0.24, 0.24, 0.25, 123.02],
    "Scale 100 (s)": [0.16, 0.51, 0.24, 0.25, 0.47, 1243.07],
    "Scale 1000 (s)": [0.17, 1.06, 0.57, 0.91, 1.47, 12942.21]
}

data_azure = {
    "Operation": ["create_database", "users", "vehicles", "drivers", "payments", "rides"],
    "Scale 1 (s)": [0.24, 0.27, 0.27, 0.27, 0.27, 28.56],
    "Scale 10 (s)": [0.28, 0.26, 0.26, 0.26, 0.26, 133.62],
    "Scale 100 (s)": [0.35, 0.54, 0.25, 0.26, 0.43, 1381.94],
    "Scale 1000 (s)": [0.28, 1.41, 0.32, 0.35, 1.76, 14078.79]
}

# Convert to DataFrame
df_google_cloud = pd.DataFrame(data_google_cloud)
df_azure = pd.DataFrame(data_azure)

# Melt the data for seaborn bar plot
df_google_cloud_melted = df_google_cloud.melt(id_vars="Operation", var_name="Scale", value_name="Execution Time (s)")
df_azure_melted = df_azure.melt(id_vars="Operation", var_name="Scale", value_name="Execution Time (s)")

# Plotting for Google Cloud
plt.figure(figsize=(12, 6))
sns.barplot(x='Operation', y='Execution Time (s)', hue='Scale', data=df_google_cloud_melted, palette='Greens_d')
plt.title('Execution Times for Google Cloud')
plt.ylabel('Execution Time (s)')
plt.xlabel('Operation')
plt.yscale('log')
plt.xticks(rotation=45)
plt.legend(title='Scale', loc='upper left')
plt.savefig('loading_google.png')

# Plotting for Azure
plt.figure(figsize=(12, 6))
sns.barplot(x='Operation', y='Execution Time (s)', hue='Scale', data=df_azure_melted, palette='Blues_d')
plt.title('Execution Times for Azure')
plt.ylabel('Execution Time (s)')
plt.xlabel('Operation')
plt.yscale('log')
plt.xticks(rotation=45)
plt.legend(title='Scale', loc='upper left')

plt.savefig('loading_azure.png')
