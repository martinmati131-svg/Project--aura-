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
