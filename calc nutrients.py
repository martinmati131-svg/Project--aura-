import datetime

def get_fertilizer_dose(months_old):
    """
    Calculates CAN/NPK dosage for young avocado trees in Kenya.
    Based on standard 150g-250g increments for the first 3 years.
    """
    if months_old < 6:
        dose = 150  # grams per tree
        type_frt = "NPK 17:17:17 (Starter)"
    elif 6 <= months_old < 12:
        dose = 250
        type_frt = "CAN or NPK 26:0:0"
    elif 12 <= months_old < 24:
        dose = 500
        type_frt = "CAN + Organic Manure (2 buckets)"
    else:
        dose = 1000
        type_frt = "Full NPK + Micronutrients"
        
    return dose, type_frt

# Input the age of your seedlings
tree_age_months = 5 
amount, fertilizer = get_fertilizer_dose(tree_age_months)

print(f"--- Project Aura Nutrient Report ---")
print(f"Tree Age: {tree_age_months} months")
print(f"Recommended Dosage: {amount}g per tree")
print(f"Fertilizer Type: {fertilizer}")
print(f"Total for 50 trees: {(amount * 50) / 1000} kg")
from datetime import datetime

# 1. SET YOUR PLANTING DATE (Year, Month, Day)
# Change this to the actual date you put your Hass/Fuerte in the ground
PLANTING_DATE = datetime(2025, 10, 15) 

def calculate_age_months(start_date):
    today = datetime.now()
    # Calculate difference in years and months
    years = today.year - start_date.year
    months = today.month - start_date.month
    return (years * 12) + months

def get_fertilizer_report(months_old):
    if months_old < 6:
        dose, type_frt = 150, "NPK 17:17:17 (Starter)"
    elif 6 <= months_old < 12:
        dose, type_frt = 250, "CAN or NPK 26:0:0"
    elif 12 <= months_old < 24:
        dose, type_frt = 500, "CAN + Organic Manure"
    else:
        dose, type_frt = 1000, "Full NPK + Micronutrients"
    return dose, type_frt

# --- Execution ---
age = calculate_age_months(PLANTING_DATE)
amount, fertilizer = get_fertilizer_report(age)

print(f"--- PROJECT AURA: ORCHARD INTELLIGENCE ---")
print(f"Status: Monitoring Hass & Fuerte Block")
print(f"Tree Age: {age} months")
print(f"Recommended Action: Apply {amount}g of {fertilizer} per tree.")
print(f"Next Stage: {12 - age if age < 12 else 'Mature Phase'} months until next dosage increase.")
