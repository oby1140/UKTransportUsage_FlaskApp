import pandas as pd
import random
from datetime import datetime, timedelta

# Define test data fields and types
test_data_fields = {
    "date": "datetime",
    "transportMode": "string",
    "usageIndicator": "float"
}

# Sample transport modes
transport_modes = ["cars", "national_rail", "bus", "tram", "cycling", "walking"]

# Generate realistic test data
def generate_test_data(num_records=50):
    test_data = []
    start_date = datetime(2015, 1, 1)
    
    for i in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 3650))  # Random date within 10 years
        transport_mode = random.choice(transport_modes)
        usage_indicator = round(random.uniform(0.5, 1.5), 2)  # Simulating normal usage fluctuations
        
        test_data.append({
            "Test Case #": i + 1,
            "Type": "Positive" if usage_indicator >= 0.8 else "Negative",
            "Date": date.strftime("%Y-%m-%d"),
            "Transport Mode": transport_mode,
            "Usage Indicator": usage_indicator,
            "Expected Result": "Valid data should be processed correctly" if usage_indicator >= 0.8 else "System should handle low usage gracefully"
        })
    
    # Add boundary cases
    boundary_cases = [
        {"Test Case #": num_records + 1, "Type": "Boundary", "Date": "2015-01-01", "Transport Mode": "cars", "Usage Indicator": 0.8, "Expected Result": "Edge case at 0.8 should be valid"},
        {"Test Case #": num_records + 2, "Type": "Boundary", "Date": "2025-12-31", "Transport Mode": "bus", "Usage Indicator": 1.5, "Expected Result": "Edge case at 1.5 should be valid"},
        {"Test Case #": num_records + 3, "Type": "Boundary", "Date": "2020-06-15", "Transport Mode": "tram", "Usage Indicator": 0.5, "Expected Result": "Edge case at 0.5 should be valid"}
    ]
    test_data.extend(boundary_cases)
    
    # Add missing/invalid data tests
    invalid_cases = [
        {"Test Case #": num_records + 4, "Type": "Negative", "Date": None, "Transport Mode": "cycling", "Usage Indicator": 1.2, "Expected Result": "Missing date should trigger an error"},
        {"Test Case #": num_records + 5, "Type": "Negative", "Date": "2022-08-12", "Transport Mode": None, "Usage Indicator": 0.9, "Expected Result": "Missing transport mode should trigger an error"},
        {"Test Case #": num_records + 6, "Type": "Negative", "Date": "2019-11-30", "Transport Mode": "bus", "Usage Indicator": "ABC", "Expected Result": "Non-numeric usage indicator should trigger an error"},
        {"Test Case #": num_records + 7, "Type": "Negative", "Date": "9999-99-99", "Transport Mode": "cars", "Usage Indicator": 1.1, "Expected Result": "Invalid date format should trigger an error"}
    ]
    test_data.extend(invalid_cases)
    
    return pd.DataFrame(test_data)


def format_test_data_output(df):
    # Set display options for better readability
    pd.set_option('display.max_rows', 20)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    
    # Format the output
    print("\n=== UK Transport Usage Test Data ===\n")
    
    # Show test case summary
    print("Test Case Overview:")
    print(f"Total number of test cases: {len(df)}")
    print(f"Positive test cases: {len(df[df['Type'] == 'Positive'])}")
    print(f"Negative test cases: {len(df[df['Type'] == 'Negative'])}")
    print(f"Boundary test cases: {len(df[df['Type'] == 'Boundary'])}\n")
    
    # Show transport mode distribution
    print("Transport Mode Distribution:")
    print(df['Transport Mode'].value_counts())
    print("\n=== Detailed Test Data ===\n")
    
    # Sort by test case number and show all data
    print(df.sort_values('Test Case #').to_string())

# Generate test dataset
test_df = generate_test_data(100)

# Display formatted test data
format_test_data_output(test_df)