import pandas as pd

# Load the dataset
file_list = pd.read_csv('/home/trin4156/Downloads/EchoNet-Dynamic/FileList.csv')
# Create two copies of the file_list for each cycle (ED and ES)
ed_data = file_list.copy()
es_data = file_list.copy()

# Add '_ED' and '_ES' suffixes to the file names
ed_data['FileName'] += '_ED'
es_data['FileName'] += '_ES'

# Assign 'ED' and 'ES' to the 'cycle' column
ed_data['cycle'] = 'ED'
es_data['cycle'] = 'ES'

# Combine ED and ES data into one DataFrame
combined_data = pd.concat([ed_data, es_data], ignore_index=True)

# Generate metadata DataFrame
metadata = pd.DataFrame({
    'file_name': combined_data['FileName'],
    'source': 'echonet',
    'echo_type': 'TTE',
    'view': 'a4ch',
    'quality': 'X',
    'EF': combined_data['EF'],
    'cycle': combined_data['cycle'],
    'split': combined_data['Split']
})

# Print the resulting DataFrame
print(metadata.head())

# Optionally, save the metadata to a new CSV file
metadata.to_csv('metadata.csv', index=False)
