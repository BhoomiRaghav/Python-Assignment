# ---------------------------------------------------------
# Project: GradeBook Analyzer
# Author: [Bhoomi Raghav]
# Date: [22/11/2025]
# Course: Programming for Problem Solving using Python
# Assignment: Lab Assignment 2
# ---------------------------------------------------------

import csv
import os

def calculate_average(marks_list):
    """Calculates the arithmetic mean of marks."""
    if not marks_list:
        return 0.0
    return sum(marks_list) / len(marks_list)

def calculate_median(marks_list):
    """Calculates the median score."""
    if not marks_list:
        return 0.0
    sorted_marks = sorted(marks_list)
    n = len(sorted_marks)
    mid = n // 2
    
    if n % 2 == 1:
        return sorted_marks[mid]
    else:
        return (sorted_marks[mid - 1] + sorted_marks[mid]) / 2

def find_max_score(marks_dict):
    """Finds the student(s) with the highest score."""
    if not marks_dict:
        return 0, []
    max_score = max(marks_dict.values())
    top_students = [name for name, score in marks_dict.items() if score == max_score]
    return max_score, top_students

def find_min_score(marks_dict):
    """Finds the student(s) with the lowest score."""
    if not marks_dict:
        return 0, []
    min_score = min(marks_dict.values())
    low_students = [name for name, score in marks_dict.items() if score == min_score]
    return min_score, low_students

def assign_grade(score):
    """Assigns a letter grade based on the score."""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def load_from_csv(filename):
    """Reads student data from a CSV file."""
    marks_dict = {}
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header if present
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    try:
                        score = float(row[1])
                        marks_dict[name] = score
                    except ValueError:
                        print(f"Warning: Invalid score for {name}, skipping.")
        print(f"Successfully loaded {len(marks_dict)} records.")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return marks_dict

def get_manual_input():
    """Gets student data via manual user entry."""
    marks_dict = {}
    print("\n--- Manual Data Entry ---")
    print("Type 'done' as the name to finish.")
    
    while True:
        name = input("Enter Student Name: ").strip()
        if name.lower() == 'done':
            break
        if not name:
            print("Name cannot be empty.")
            continue
            
        try:
            score_input = input(f"Enter marks for {name}: ")
            score = float(score_input)
            if 0 <= score <= 100:
                marks_dict[name] = score
            else:
                print("Please enter a score between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for marks.")
            
    return marks_dict

def analyze_and_report(marks_dict):
    """Performs analysis and prints the report table."""
    if not marks_dict:
        print("No data to analyze.")
        return

    print("\n" + "="*50)
    print(f"{'Name':<20} | {'Marks':<10} | {'Grade':<5}")
    print("-" * 50)

    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    
    # Process each student
    for name, score in marks_dict.items():
        grade = assign_grade(score)
        grade_counts[grade] += 1
        print(f"{name:<20} | {score:<10.1f} | {grade:<5}")
        
    print("="*50)

    # Statistical Analysis
    scores = list(marks_dict.values())
    avg_score = calculate_average(scores)
    median_score = calculate_median(scores)
    max_val, max_students = find_max_score(marks_dict)
    min_val, min_students = find_min_score(marks_dict)
    
    # List Comprehensions for Pass/Fail
    passed = [name for name, s in marks_dict.items() if s >= 40]
    failed = [name for name, s in marks_dict.items() if s < 40]

    # Summary Output
    print("\n--- Class Summary ---")
    print(f"Total Students: {len(marks_dict)}")
    print(f"Average Score : {avg_score:.2f}")
    print(f"Median Score  : {median_score:.2f}")
    print(f"Highest Score : {max_val} ({', '.join(max_students)})")
    print(f"Lowest Score  : {min_val} ({', '.join(min_students)})")
    
    print("\n--- Grade Distribution ---")
    for g, count in grade_counts.items():
        print(f"Grade {g}: {count} student(s)")
        
    print("\n--- Performance Status ---")
    print(f"Passed: {len(passed)} students")
    print(f"Failed: {len(failed)} students ({', '.join(failed)})")

def main():
    print("Welcome to the GradeBook Analyzer CLI")
    
    while True:
        print("\nMain Menu:")
        print("1. Enter Marks Manually")
        print("2. Load Marks from CSV")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        marks_data = {}
        
        if choice == '1':
            marks_data = get_manual_input()
            analyze_and_report(marks_data)
        elif choice == '2':
            filename = input("Enter CSV filename (e.g., sample_data.csv): ").strip()
            marks_data = load_from_csv(filename)
            if marks_data:
                analyze_and_report(marks_data)
        elif choice == '3':
            print("Exiting GradeBook Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()