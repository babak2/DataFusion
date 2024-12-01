"""
Data Fusion Script

# This script performs data fusion on population and energy price data.
It loads population data, filters it based on specific criteria, preprocesses it by melting and interpolating,
loads energy price data, merges the population & energy price data, & saves the combined data to a CSV file.

Author: Babak Mahdavi Ardestani

"""

import os
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)


def load_population_data(file_path):
    """
    Load population data from a CSV file.

    Parameters:
    - file_path (str): Path to the population data CSV file.

    Returns:
    - pd.DataFrame: DataFrame containing the population data.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Population data file not found: {file_path}")
    return pd.read_csv(file_path)


def filter_population_data(pop_data):
    """
    Filter population data for a specific MODEL and SCENARIO.

    Parameters:
    - pop_data (pd.DataFrame): DataFrame containing the population data.

    Returns:
    - pd.DataFrame: Filtered DataFrame containing the population data.
    """
    return pop_data[(pop_data['MODEL'] == 'IIASA-WiC POP') & (pop_data['SCENARIO'] == 'SSP3_v9_130115')]


def preprocess_population_data(filtered_pop_data):
    """
    Preprocess filtered population data by melting and converting year column.

    Parameters:
    - filtered_pop_data (pd.DataFrame): Filtered DataFrame containing the population data.

    Returns:
    - pd.DataFrame: Preprocessed DataFrame with 'year' and 'pop' columns.
    """
    melted_pop_data = filtered_pop_data.melt(
        id_vars=['MODEL', 'SCENARIO', 'REGION', 'UNIT', 'VAR1', 'VAR2', 'VAR3', 'VAR4'],
        var_name='year', value_name='pop'
    )
    melted_pop_data['year'] = melted_pop_data['year'].astype(int)
    return melted_pop_data


def interpolate_population_data(melted_pop_data):
    """
    Interpolate population data for the years 2020 to 2099.

    Parameters:
    - melted_pop_data (pd.DataFrame): DataFrame containing the melted population data.

    Returns:
    - pd.DataFrame: DataFrame with interpolated population values.
    """
    years = np.arange(2020, 2100)
    interpolated_population = pd.DataFrame(index=years)
    for region in melted_pop_data['REGION'].unique():
        region_data = melted_pop_data[melted_pop_data['REGION'] == region]
        interpolated_values = np.interp(
            years, region_data['year'], region_data['pop']
        )
        interpolated_population[region] = interpolated_values
    interpolated_population = interpolated_population.transpose().reset_index()
    interpolated_population = pd.melt(interpolated_population, id_vars=['index'], var_name='year', value_name='pop')
    interpolated_population.rename(columns={'index': 'REGION'}, inplace=True)
    return interpolated_population


def load_energy_price_data(file_path):
    """
    Load energy price data from a STATA file.

    Parameters:
    - file_path (str): Path to the energy price data STATA file.

    Returns:
    - pd.DataFrame: DataFrame containing the energy price data.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Energy price data file not found: {file_path}")
    return pd.read_stata(file_path)


def merge_data(interpolated_population, energy_price_data):
    """
    Merge interpolated population data & energy price data.

    Parameters:
    - interpolated_population (pd.DataFrame): DataFrame containing interpolated population data.
    - energy_price_data (pd.DataFrame): DataFrame containing energy price data.

    Returns:
    - pd.DataFrame: Combined DataFrame with population & energy price data.
    """
    combined_data = pd.merge(interpolated_population, energy_price_data, left_on=['REGION', 'year'],
                             right_on=['country', 'year'])
    return combined_data[['year', 'pop', 'country', 'other_energycompile_price',
                          'electricitycompile_price', 'electricitycompile_peakprice']]


def save_data(final_data, output_dir, output_file_name):
    """
    Save combined data to CSV file.

    Parameters:
    - final_data (pd.DataFrame): DataFrame containing the combined data.
    - output_dir (str): Output directory path.
    - output_file_name (str): Output file name.

    Returns:
    - None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file_path = os.path.join(output_dir, output_file_name)
    final_data.to_csv(output_file_path, index=False)
    print("Data saved to:", output_file_path)


############
#    MAIN
############

if __name__ == "__main__":
    # Input file paths
    pop_file_path = 'data/population.csv'
    energy_price_file_path = 'data/IEA_Price_FIN_Clean_gr014_GLOBAL.dta'

    # Output directory & file name
    output_dir = 'output'
    output_file_name = 'valinfo.csv'

    # Load population data
    pop_data = load_population_data(pop_file_path)

    # Filter population data
    filtered_pop_data = filter_population_data(pop_data)

    # Preprocess population data
    melted_pop_data = preprocess_population_data(filtered_pop_data)

    # Interpolate population data
    interpolated_population = interpolate_population_data(melted_pop_data)

    # Load energy price data
    energy_price_data = load_energy_price_data(energy_price_file_path)

    # Merge population and energy price data
    combined_data = merge_data(interpolated_population, energy_price_data)

    # Save the combine data
    save_data(combined_data, output_dir, output_file_name)













