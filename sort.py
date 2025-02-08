import json

# Load the JSON data from a file
with open('my_data.json', 'r') as file:
    json_data = json.load(file)

# List of EUI IDs to filter
eui_filter = ["24E124707E238848"]

# Filter the JSON data based on the EUI values
filtered_data = [entry for entry in json_data if entry.get('EUI') in eui_filter]

# Output the filtered data
output_file = 'filtered_data.json'
with open(output_file, 'w') as file:
    json.dump(filtered_data, file, indent=4)

print(f"Filtered data saved to {output_file}")
