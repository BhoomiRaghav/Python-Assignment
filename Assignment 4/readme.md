Weather Data Visualizer Project (Lab Assignment 4)

Name: Bhoomi Raghav
Roll Number: 2501730254
Course: Programming for Problem Solving using Python
Date: 04/12/2025

Project Objective

This project implements a complete data analysis and visualization pipeline for real-world weather data using Python's fundamental data science libraries (Pandas, NumPy, and Matplotlib). The goal is to ingest raw data, clean it, perform statistical aggregation, visualize key trends, and generate a final summary report.

Tools and Libraries Used

Pandas: Used for data loading, cleaning, processing (handling NaNs, converting types), time-series analysis (resample), and calculating descriptive statistics.

NumPy: Utilized implicitly by Pandas for high-performance numerical operations (mean, min, max, sum).

Matplotlib: Used for generating informative charts (Line Plot, Bar Plot, Scatter Plots).

Pathlib: Used for robust file and directory management.

Results and Deliverables

The script successfully generated the following output files, which are submitted alongside this README:

cleaned_weather_data.csv: The processed dataset, indexed by the cleaned Date column, with missing values handled.

weather_summary.md: A textual report summarizing the key statistical findings and interpretations.

plots/ directory (containing the following PNG images):

plots/temp_trend_line.png: Line chart showing the daily maximum and minimum temperature trends over the period.

plots/monthly_rainfall_bar.png: Bar chart displaying the total accumulated rainfall for each month.

plots/combined_scatter_plots.png: A multi-plot figure showing the relationship between maximum/minimum temperature and humidity.

Key Insights from Analysis

The analysis focuses on identifying seasonal patterns and correlations, as detailed in the weather_summary.md.

Temperature Trends: [Describe the observed trend here, e.g., "The daily trend line clearly shows temperatures rising consistently, with the period ending in June showing the highest peak temperatures."]

Rainfall Patterns: [Reference the peak month found in the summary, e.g., "Rainfall is highly seasonal, with a significant spike observed in June, indicating the start of the monsoon or wet season."]

Correlation: [Describe the Humidity vs. Temp observation, e.g., "The scatter plots suggest an inverse relationship between temperature and humidity, where the highest humidity levels often align with lower temperatures (or the rainy season)."]
