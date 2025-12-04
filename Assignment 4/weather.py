# Name: Bhoomi Raghav
# Roll number: 2501730254
# Course Code: ETCCPP102
# Assignment: Weather Data Visualizer
# Date: 2025-12-08

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- Configuration ---
# NOTE: Ensure you have a 'sample_weather_data.csv' file in the same directory.
DATA_FILE = 'sample_weather_data.csv'
CLEANED_FILE = 'cleaned_weather_data.csv'
OUTPUT_DIR = Path('plots')

def data_acquisition_and_loading(filepath):
    """Task 1: Load and inspect data."""
    print(f"--- Task 1: Loading Data from {filepath} ---")
    try:
        df = pd.read_csv(filepath)
        print("Initial DataFrame Head:")
        print(df.head())
        print("\nInitial DataFrame Info:")
        df.info()
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {filepath}")
        print("ACTION REQUIRED: Please ensure 'sample_weather_data.csv' is in the same directory as this script.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during file reading: {e}")
        return None


def data_cleaning_and_processing(df):
    """Task 2: Handle missing values and format dates."""
    if df is None: return None
    print("\n--- Task 2: Cleaning Data ---")
    
    # Drop rows with any NaN values for simplicity in this dataset
    df_cleaned = df.dropna()
    print(f"Dropped {len(df) - len(df_cleaned)} rows with missing values.")
    
    # Convert Date column to datetime format. 'errors=coerce' turns invalid dates into NaT.
    df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'], errors='coerce')
    # Drop any rows where date conversion failed (NaT)
    df_cleaned = df_cleaned.dropna(subset=['Date'])
    
    # Set Date as index
    df_cleaned = df_cleaned.set_index('Date')
    
    # Filter for relevant columns
    df_cleaned = df_cleaned[['Max Temp (°C)', 'Min Temp (°C)', 'Rainfall (mm)', 'Humidity (%)']]
    
    print("\nCleaned DataFrame Head:")
    print(df_cleaned.head())
    df_cleaned.info()
    return df_cleaned

def statistical_analysis(df):
    """Task 3: Compute daily/monthly statistics using NumPy concepts (via Pandas)."""
    if df is None: return None
    print("\n--- Task 3: Statistical Analysis (NumPy/Pandas) ---")
    
    # Overall Daily Descriptive Statistics
    daily_stats = df.describe().T[['mean', 'min', 'max', 'std']]
    print("\nOverall Descriptive Statistics:")
    print(daily_stats)
    
    # Monthly Statistics using resample and NumPy functions (Aggregation)
    # NOTE: Using 'ME' (Month End) instead of 'M' to remove FutureWarning, and using strings 
    # for aggregation functions to remove other FutureWarnings.
    monthly_stats = df.resample('ME').agg({
        'Max Temp (°C)': ['mean', 'min', 'max'],
        'Rainfall (mm)': 'sum',
        'Humidity (%)': 'mean'
    })
    # Flatten column names for easier access in the report generation
    monthly_stats.columns = ['_'.join(col).strip() for col in monthly_stats.columns.values]
    
    print("\nMonthly Aggregated Statistics:")
    print(monthly_stats)
    return daily_stats, monthly_stats

def visualization(df):
    """Task 4: Create informative plots using Matplotlib."""
    if df is None: return
    print("\n--- Task 4: Generating Visualizations (Plots saved to 'plots' directory) ---")

    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 1. Line chart for daily temperature trends
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Max Temp (°C)'], label='Max Temp', color='#FF5733', linewidth=2, alpha=0.8)
    plt.plot(df.index, df['Min Temp (°C)'], label='Min Temp', color='#3375FF', linewidth=2, linestyle='--')
    plt.title('Daily Temperature Trend (Max and Min)', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.legend(frameon=True, shadow=True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'temp_trend_line.png')
    plt.close()
    print("- Saved: temp_trend_line.png")

    # 2. Bar chart for monthly rainfall totals (Task 5: Grouping/Aggregation)
    # FIX: We must calculate monthly rainfall using resample(..) here, as the 'df' passed is the daily data.
    monthly_rainfall = df['Rainfall (mm)'].resample('ME').sum()
    monthly_rainfall.index = monthly_rainfall.index.strftime('%Y-%m') # Format month for readability
    plt.figure(figsize=(8, 5))
    plt.bar(monthly_rainfall.index, monthly_rainfall.values, color='#00A8E8', edgecolor='black', alpha=0.9)
    plt.title('Monthly Rainfall Totals', fontsize=14, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Rainfall (mm)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'monthly_rainfall_bar.png')
    plt.close()
    print("- Saved: monthly_rainfall_bar.png")

    # 3. Combined Scatter Plot (Bonus/Task 4 Advanced Plotting)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Scatter Plot 1: Max Temp vs Humidity
    axes[0].scatter(df['Max Temp (°C)'], df['Humidity (%)'], color='#8D4585', alpha=0.7, edgecolors='gray', linewidths=0.5)
    axes[0].set_title('Humidity vs. Max Temperature')
    axes[0].set_xlabel('Max Temperature (°C)')
    axes[0].set_ylabel('Humidity (%)')
    axes[0].grid(True, linestyle='--')
    
    # Scatter Plot 2: Min Temp vs Humidity
    axes[1].scatter(df['Min Temp (°C)'], df['Humidity (%)'], color='#FFA500', alpha=0.7, edgecolors='gray', linewidths=0.5)
    axes[1].set_title('Humidity vs. Min Temperature')
    axes[1].set_xlabel('Min Temperature (°C)')
    axes[1].set_ylabel('Humidity (%)')
    axes[1].grid(True, linestyle='--')

    plt.suptitle('Combined Weather Visualizations (Temperature-Humidity Relationship)', fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to make room for suptitle
    plt.savefig(OUTPUT_DIR / 'combined_scatter_plots.png')
    plt.close()
    print("- Saved: combined_scatter_plots.png (Contains two plots in one figure)")


def export_and_storytelling(df, daily_stats, monthly_stats):
    """Task 6: Export cleaned data and create a summary."""
    if df is None: return
    print("\n--- Task 6: Exporting Data and Generating Summary Report ---")
    
    # Export cleaned data
    df.to_csv(CLEANED_FILE)
    print(f"- Cleaned data exported to {CLEANED_FILE}")
    
    # Find peak rainfall month for the summary (using the flattened column names)
    peak_rainfall_sum = monthly_stats['Rainfall (mm)_sum'].max()
    peak_rainfall_month = monthly_stats['Rainfall (mm)_sum'].idxmax().strftime('%B')
    
    # Find the maximum recorded temperature
    max_temp_overall = daily_stats.loc['Max Temp (°C)', 'max']
    
    # Generate Summary Report (Markdown/Text)
    report_path = Path('weather_summary.md')
    
    summary_text = f"""# Weather Data Analysis Report

## 1. Overview
This report analyzes local weather data from {df.index.min().strftime('%B %Y')} to {df.index.max().strftime('%B %Y')}.

## 2. Key Statistical Insights (Daily Averages)

| Metric | Max Temp (°C) | Min Temp (°C) | Rainfall (mm) | Humidity (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Mean** | {daily_stats.loc['Max Temp (°C)', 'mean']:.2f} | {daily_stats.loc['Min Temp (°C)', 'mean']:.2f} | {daily_stats.loc['Rainfall (mm)', 'mean']:.2f} | {daily_stats.loc['Humidity (%)', 'mean']:.2f} |
| **Max** | {daily_stats.loc['Max Temp (°C)', 'max']:.2f} | {daily_stats.loc['Min Temp (°C)', 'max']:.2f} | {daily_stats.loc['Rainfall (mm)', 'max']:.2f} | {daily_stats.loc['Humidity (%)', 'max']:.2f} |

## 3. Trend Interpretation (Storytelling)
- **Temperature:** The daily line chart shows a clear seasonal increase in temperature, indicating the transition from cooler to warmer seasons. The maximum recorded temperature across the period was **{max_temp_overall:.1f} °C**.
- **Rainfall:** The bar chart highlights that rainfall is highly seasonal. The data shows significant rainfall spikes in {peak_rainfall_month}, suggesting the onset of the wet season.
- **Humidity vs. Temperature:** The scatter plots visually confirm an inverse relationship: as Max Temperature increases, Humidity tends to decrease. This suggests that the highest humidity levels are primarily observed during the cooler, rainy periods.

## 4. Aggregation Highlight
- **Peak Rainfall Month:** {peak_rainfall_month} showed the highest total rainfall of **{peak_rainfall_sum:.2f} mm**.
"""
    
    try:
        with report_path.open('w', encoding='utf-8') as f:
            f.write(summary_text)
    except Exception as e:
        print(f"Error writing summary report: {e}")
        return

    print(f"- Summary report saved to {report_path}")


def main():
    """Main execution function to run all analysis tasks."""
    df_raw = data_acquisition_and_loading(DATA_FILE)
    
    if df_raw is None:
        print("\nProject terminated due to failure in data acquisition.")
        return

    df_cleaned = data_cleaning_and_processing(df_raw)
    
    if df_cleaned is not None:
        # Calculate statistics
        # daily_stats and monthly_stats are created here
        daily_stats, monthly_stats = statistical_analysis(df_cleaned)
        
        # Generate visualizations (now correctly calculates monthly rainfall inside)
        visualization(df_cleaned)
        
        # Export data and generate the report
        export_and_storytelling(df_cleaned, daily_stats, monthly_stats)
        
        print("\nWeather Data Visualization project completed successfully.")
    else:
        print("\nProject terminated due to data cleaning errors.")

if __name__ == "__main__":
    main()