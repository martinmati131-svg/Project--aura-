import datetime

def check_orchard_health(moisture_level):
    """
    Analyzes moisture and returns a status for Hass/Fuerte seedlings.
    Input: moisture_level (0-100%)
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if moisture_level < 30:
        status = "CRITICAL: Soil is too dry. Irrigation required immediately."
        recommendation = "Check drip lines for blockages."
    elif 30 <= moisture_level <= 60:
        status = "OPTIMAL: Soil moisture is perfect for root growth."
        recommendation = "Maintain current schedule."
    else:
        status = "WARNING: Soil is saturated. Risk of root rot."
        recommendation = "Reduce irrigation frequency."

    log_entry = f"[{timestamp}] Level: {moisture_level}% | Status: {status} | Action: {recommendation}\n"
    
    # Save locally to the file we created earlier
    with open("orchard_logs.txt", "a") as file:
        file.write(log_entry)
        
    return status

# Example usage (Assuming your sensor reads 25%):
current_status = check_orchard_health(25)
print(f"Update: {current_status}")
