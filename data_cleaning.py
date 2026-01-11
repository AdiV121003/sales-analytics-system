"""
Sales Data Cleaning Script
Cleans and validates sales transaction data from sales_data.txt
"""

import re
import pandas as pd

def clean_sales_data(input_file='sales_data.txt', output_file='cleaned_sales_data.csv'):
    """
    Clean sales data by removing invalid records and fixing data quality issues
    
    Invalid Records (REMOVE):
    - Missing CustomerID or Region
    - Quantity <= 0
    - UnitPrice <= 0
    - TransactionID not starting with 'T'
    
    Valid Records (CLEAN and KEEP):
    - Remove commas from ProductName
    - Remove commas from numbers (e.g., 1,500 -> 1500)
    - Skip empty lines
    """
    
    # Counters
    total_parsed = 0
    invalid_removed = 0
    valid_records = []
    
    # Column names
    columns = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
               'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    print("Starting data cleaning process...")
    print("="*60)
    
    try:
        # Read file with proper encoding handling
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
        
        # Skip header line and process data
        for line_num, line in enumerate(lines[1:], start=2):
            # Skip empty lines
            line = line.strip()
            if not line:
                continue
            
            total_parsed += 1
            
            # Split by pipe delimiter
            fields = line.split('|')
            
            # Check if we have correct number of fields
            if len(fields) != 8:
                print(f"Line {line_num}: Invalid number of fields ({len(fields)} fields) - REMOVED")
                invalid_removed += 1
                continue
            
            # Extract fields
            transaction_id = fields[0].strip()
            date = fields[1].strip()
            product_id = fields[2].strip()
            product_name = fields[3].strip()
            quantity_str = fields[4].strip()
            unit_price_str = fields[5].strip()
            customer_id = fields[6].strip()
            region = fields[7].strip()
            
            # Validation flags
            is_valid = True
            removal_reason = []
            
            # Rule 1: TransactionID must start with 'T'
            if not transaction_id.startswith('T'):
                is_valid = False
                removal_reason.append("Invalid TransactionID format")
            
            # Rule 2: CustomerID cannot be missing
            if not customer_id:
                is_valid = False
                removal_reason.append("Missing CustomerID")
            
            # Rule 3: Region cannot be missing
            if not region:
                is_valid = False
                removal_reason.append("Missing Region")
            
            # Rule 4: Quantity must be > 0
            try:
                # Clean commas from quantity
                quantity_clean = quantity_str.replace(',', '')
                quantity = int(quantity_clean)
                if quantity <= 0:
                    is_valid = False
                    removal_reason.append(f"Invalid Quantity ({quantity} <= 0)")
            except ValueError:
                is_valid = False
                removal_reason.append(f"Invalid Quantity format: {quantity_str}")
            
            # Rule 5: UnitPrice must be > 0
            try:
                # Clean commas from price
                price_clean = unit_price_str.replace(',', '')
                unit_price = float(price_clean)
                if unit_price <= 0:
                    is_valid = False
                    removal_reason.append(f"Invalid UnitPrice ({unit_price} <= 0)")
            except ValueError:
                is_valid = False
                removal_reason.append(f"Invalid UnitPrice format: {unit_price_str}")
            
            # Process record based on validity
            if not is_valid:
                print(f"Line {line_num}: {transaction_id} - {', '.join(removal_reason)} - REMOVED")
                invalid_removed += 1
            else:
                # Clean valid record
                # Remove commas from ProductName
                product_name_clean = product_name.replace(',', ' ')
                
                # Add to valid records
                valid_records.append({
                    'TransactionID': transaction_id,
                    'Date': date,
                    'ProductID': product_id,
                    'ProductName': product_name_clean,
                    'Quantity': quantity,
                    'UnitPrice': unit_price,
                    'CustomerID': customer_id,
                    'Region': region
                })
        
        # Calculate valid records
        valid_count = len(valid_records)
        
        # Print validation output
        print("\n" + "="*60)
        print("VALIDATION OUTPUT:")
        print("="*60)
        print(f"Total records parsed: {total_parsed}")
        print(f"Invalid records removed: {invalid_removed}")
        print(f"Valid records after cleaning: {valid_count}")
        print("="*60)
        
        # Save cleaned data to CSV
        if valid_records:
            df = pd.DataFrame(valid_records)
            df.to_csv(output_file, index=False)
            print(f"\n✓ Cleaned data saved to: {output_file}")
            print(f"\nSample of cleaned data:")
            print(df.head())
        else:
            print("\n✗ No valid records found!")
        
        return df if valid_records else None
        
    except FileNotFoundError:
        print(f"✗ Error: File '{input_file}' not found!")
        return None
    except Exception as e:
        print(f"✗ Error occurred: {e}")
        return None


def analyze_cleaned_data(df):
    """
    Perform basic analysis on cleaned data
    """
    if df is None or df.empty:
        print("No data to analyze!")
        return
    
    print("\n" + "="*60)
    print("DATA ANALYSIS:")
    print("="*60)
    
    # Summary statistics
    print(f"\nTotal Revenue: ₹{(df['Quantity'] * df['UnitPrice']).sum():,.2f}")
    print(f"Total Quantity Sold: {df['Quantity'].sum():,}")
    print(f"Average Transaction Value: ₹{(df['Quantity'] * df['UnitPrice']).mean():,.2f}")
    
    # By Region
    print("\n--- Sales by Region ---")
    region_sales = df.groupby('Region').agg({
        'Quantity': 'sum',
        'UnitPrice': lambda x: (df.loc[x.index, 'Quantity'] * x).sum()
    }).rename(columns={'UnitPrice': 'Revenue'})
    print(region_sales)
    
    # Top Products
    print("\n--- Top 5 Products by Revenue ---")
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    top_products = df.groupby('ProductName')['Revenue'].sum().sort_values(ascending=False).head(5)
    print(top_products)


if __name__ == "__main__":
    # Clean the data
    cleaned_df = clean_sales_data('data/sales_data.txt', 'cleaned_sales_data.csv')
    
    # Analyze cleaned data
    if cleaned_df is not None:
        analyze_cleaned_data(cleaned_df)
