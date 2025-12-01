import csv
import os
import math
from datetime import datetime

FILE_NAME = "health_history.csv"

def calculate_bmi(weight_kg, height_m):
    """Calculates BMI given weight in kg and height in meters."""
    try:
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    except ZeroDivisionError:
        return 0.0

def calculate_body_fat_navy(gender, height_cm, waist_cm, neck_cm, hip_cm=0):
    """
    Calculates Body Fat Percentage (BFP) using the U.S. Navy Method.
    """
    try:
        if gender.lower() == 'm':
            if waist_cm - neck_cm <= 0:
                return 0.0
            
            log_waist_neck = math.log10(waist_cm - neck_cm)
            log_height = math.log10(height_cm)
            
            bfp = 495 / (1.0324 - 0.19077 * log_waist_neck + 0.15456 * log_height) - 450
            
        else:
            if waist_cm + hip_cm - neck_cm <= 0:
                return 0.0

            log_waist_hip_neck = math.log10(waist_cm + hip_cm - neck_cm)
            log_height = math.log10(height_cm)
            
            bfp = 495 / (1.29579 - 0.35004 * log_waist_hip_neck + 0.22100 * log_height) - 450

        return round(max(bfp, 0), 2)
    except Exception:
        return 0.0

def get_bmi_category(bmi):
    """Returns the health category based on BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def save_record(name, age, gender, weight, height, waist, neck, hip, bmi, bfp, category):
    """Saves the record to a CSV file."""
    file_exists = os.path.isfile(FILE_NAME)
    
    try:
        with open(FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Date", "Name", "Age", "Gender", "Weight (kg)", "Height (m)", "Waist (cm)", "Neck (cm)", "Hip (cm)", "BMI", "Body Fat %", "Category"])
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, name, age, gender.upper(), weight, height, waist, neck, hip, bmi, bfp, category])
        
        print(f"\n[Success] Record for {name} saved to '{FILE_NAME}'.")
    except Exception as e:
        print(f"\n[Error] Could not save file: {e}")

def main():
    print("="*60)
    print("      COMPREHENSIVE HEALTH TRACKER (U.S. NAVY METHOD)      ")
    print("      (Requires: Weight, Height, Waist, Neck, Hip)         ")
    print("="*60)
    
    while True:
        try:
            print("\n--- New Entry ---")
            name = input("Enter Name (or type 'exit' to quit): ").strip()
            if name.lower() == 'exit':
                print("Exiting program. Stay healthy!")
                break

            age = int(input("Enter Age: "))
            gender = input("Enter Gender (M/F): ").strip().lower()
            
            while gender not in ['m', 'f']:
                print("Invalid gender. Please enter 'M' for Male or 'F' for Female.")
                gender = input("Enter Gender (M/F): ").strip().lower()

            weight = float(input("Enter Weight (in kg): "))
            height_cm = float(input("Enter Height (in cm): "))
            
            neck_cm = float(input("Enter Neck Circumference (in cm): "))
            waist_cm = float(input("Enter Waist Circumference (in cm): "))
            
            hip_cm = 0.0
            if gender == 'f':
                hip_cm = float(input("Enter Hip Circumference (in cm): "))

            if weight <= 0 or height_cm <= 0 or age <= 0:
                print("Error: Inputs must be positive numbers!")
                continue

            height_m = height_cm / 100
            bmi = calculate_bmi(weight, height_m)
            bfp = calculate_body_fat_navy(gender, height_cm, waist_cm, neck_cm, hip_cm)
            category = get_bmi_category(bmi)

            print("-" * 35)
            print(f"Results for {name}:")
            print(f"  > BMI Score      : {bmi}")
            print(f"  > Body Fat %     : {bfp}% (U.S. Navy Method)")
            print(f"  > Health Category: {category}")
            print("-" * 35)

            save_cmd = input("Do you want to save this result? (y/n): ").lower()
            if save_cmd == 'y':
                save_record(name, age, gender, weight, height_m, waist_cm, neck_cm, hip_cm, bmi, bfp, category)

        except ValueError:
            print("Invalid Input! Please enter numeric values.")

if __name__ == "__main__":
    main()