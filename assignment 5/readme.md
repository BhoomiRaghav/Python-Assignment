Capstone Project: Campus Energy-Use Dashboard

Student Name: Bhoomi Raghav
Roll Number: 2501730254
Course Code: ETCCPP102

1. Project Objective

This project implements an end-to-end data pipeline to analyze energy consumption data from multiple campus buildings. It utilizes Python's Pandas, NumPy, and Matplotlib libraries, alongside an Object-Oriented Programming (OOP) design, to ingest raw data, perform time-series aggregation, generate visualizations, and produce a summary report for administrative decision-making.

2. Setup and Execution

Prerequisites

You must have Python 3.8+ installed. The following libraries are required:

pip install -r requirements.txt


File Structure (Crucial)

The script relies on the following directory structure:

campus-energy-dashboard-<yourname>/
├── energyusedashboardpipeline.py  (Main script)
├── README.md
├── requirements.txt
├── data/                          <-- INPUT CSV files go here (MANDATORY)
└── output/                        <-- OUTPUT files are created here (MANDATORY)


Before running: Ensure the data/ folder exists and contains the sample CSV files (Science_Lab.csv and Admin_Building.csv).

Running the Pipeline

Execute the main script from the root directory of the project:

python energyusedashboardpipeline.py


3. Deliverables and Output

Upon successful execution, the script will create the output/ folder and generate the following four required files:

Filename

Type

Task

Description

dashboard.png

PNG

Task 4

Multi-chart visualization of daily trends, average weekly consumption, and hourly peak load.

building_summary.csv

CSV

Task 5

A summarized CSV table showing total, mean, min, and max consumption per building.

cleaned_energy_data.csv

CSV

Task 5

The combined, cleaned, and validated raw data used for analysis.

executive_summary.txt

TXT

Task 5

A textual summary identifying the highest consumer, peak load time, and general trends.

4. Key Implementation Details

Data Ingestion: The ingest_data function uses pathlib.glob to automatically discover and merge multiple CSV files in the data/ directory. It includes error handling (on_bad_lines='skip') and data type validation.

OOP Design: The MeterReading and Building classes model the physical system, while the BuildingManager aggregates the results, demonstrating encapsulation and modularity (Task 3).

Aggregation: Time-series analysis is performed using Pandas resample('D') for daily totals and resample('W') for weekly metrics (Task 2).

Visualization: Matplotlib is used to generate a 2x2 subplot dashboard, fulfilling the multi-chart requirement (Task 4).
