"""
CSV File Comparison Script for takk1 

This script compares two CSV files to determine if they contain the same data.
It reads the files, ensures they have the same columns, sorts them, & then compares the content.
If there are differences, it prints them out for further inspection.

Author: Babak Mahdavi Ardestani

"""

import pandas as pd

# File paths
generated_file_path = 'output/valinfo.csv' 
original_file_path = 'data/valinfo_orig.csv'

# Read the generated CSV file
generated_data = pd.read_csv(generated_file_path)

# Read the original CSV file
original_data = pd.read_csv(original_file_path)

# Print shapes for debugging
print(f"Shape of generated data: {generated_data.shape}")
print(f"Shape of original data: {original_data.shape}")

# Ensure both DataFrames have the same columns
generated_data = generated_data[original_data.columns]

# Print columns for debugging
print(f"Columns in generated data: {generated_data.columns}")
print(f"Columns in original data: {original_data.columns}")

# Sort both DataFrames by 'year' and 'country'
generated_data_sorted = generated_data.sort_values(by=['year', 'country']).reset_index(drop=True)
original_data_sorted = original_data.sort_values(by=['year', 'country']).reset_index(drop=True)

# Print shapes after sorting for debugging
print(f"Shape of sorted generated data: {generated_data_sorted.shape}")
print(f"Shape of sorted original data: {original_data_sorted.shape}")

# Compare the DataFrames
comparison_result = generated_data_sorted.equals(original_data_sorted)

if comparison_result:
    print("The files contain the same data.")
else:
    print("The files do not contain the same data.")
    
    # Align the DataFrames and compare them
    diff = generated_data_sorted.compare(original_data_sorted, align_axis=0)
    print("Differences between the files:")
    print(diff)
