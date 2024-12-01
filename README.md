# Data Fusion & Files Comparison

## Overview
This Python script processes and combines population and energy price data into a unified file named valinfo.csv. 
The population data in the resulting output file will pertain to MODEL IIASA-WiC POP and SCENARIO SSP3 v9 130115. 

The program consists of two scripts:

1. `data-fusion.py` - This main script processes population and energy price data, merges them, & saves the combined data to a CSV file.
2. `compare-files.py` - This script compares the generated CSV file with an original CSV file to ensure the data is consistent.


## Data files:

Data files (located in data directory): 

1. `IEA_Price_FIN_Clean_gr014_GLOBAL.dta` (input file: this is a STATA dataset)
2. `population.csv` (input file)
3. `valinfo_orig.csv` (this is the original valinfo file to be used for comparasion with the generated output)

## Prerequisites

- Python 3.x
- pandas
- numpy
- warnings
- os

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/babak2/DataFusion.git
    cd DataFusion
    ```

2. Install the required Python packages:

    ```
    pip install pandas numpy
    ```

## Usage

### DataFusion Script

1. **Description:**
   - The `data-fusion.py` script loads population data and energy price data, processes and merges them, & saves the result to a CSV file in the output directory.

2. **Running the Script:**

  If Python 3 is the only Python version installed on your machine, you can use the `python` command. For example:

   ```
   python data-fusion.py
   ```
  
  If both Python 2 and 3 are both installed, it's important to specify Python 3 using the `python3` command. For example:

   ```
   python3 data-fusion.py
   ```


4. **Output:**
   - The combined data is saved as `valinfo.csv` in the `output` directory.

### Compare Files 

1. **Description:**
   - The `compare-files.py` script compares the generated CSV file (`output/valinfo.csv`) with the original CSV file (`data/valinfo_orig.csv`) to ensure they contain the same data.

2. **Running the Script:**

    ```
    python3 compare-files.py
    ```

3. **Output:**
   - The script prints (to the terminal) whether the files contain the same data or not. If there are differences, it prints the differences between the files.


## Contact 

Babak Mahdavi Aresetani

babak.m.ardestani@gmail.com
