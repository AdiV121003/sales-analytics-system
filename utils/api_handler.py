"""
API Handler Module
Handles fetching product data from DummyJSON API
"""

import requests
import time
import os
import re

# API Base URL
BASE_URL = "https://dummyjson.com/products"

def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    Returns: list of product dictionaries
    
    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]
    
    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    
    print("\n" + "="*60)
    print("FETCHING PRODUCTS FROM API")
    print("="*60)
    
    try:
        # Construct URL with limit parameter
        url = f"{BASE_URL}?limit=100"
        
        print(f"Requesting: {url}")
        
        # Make GET request
        response = requests.get(url, timeout=10)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Extract products list
        products = data.get('products', [])
        
        # Format products to include only required fields
        formatted_products = []
        for product in products:
            formatted_product = {
                'id': product.get('id'),
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'price': product.get('price'),
                'rating': product.get('rating')
            }
            formatted_products.append(formatted_product)
        
        print(f"✓ SUCCESS: Fetched {len(formatted_products)} products")
        print("="*60)
        
        return formatted_products
        
    except requests.exceptions.ConnectionError:
        print("✗ FAILURE: Could not connect to API (Check internet connection)")
        print("="*60)
        return []
    
    except requests.exceptions.Timeout:
        print("✗ FAILURE: Request timed out (API took too long to respond)")
        print("="*60)
        return []
    
    except requests.exceptions.HTTPError as e:
        print(f"✗ FAILURE: HTTP Error - {e}")
        print("="*60)
        return []
    
    except requests.exceptions.RequestException as e:
        print(f"✗ FAILURE: Request error - {e}")
        print("="*60)
        return []
    
    except Exception as e:
        print(f"✗ FAILURE: Unexpected error - {e}")
        print("="*60)
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Parameters: api_products from fetch_all_products()
    Returns: dictionary mapping product IDs to info
    
    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    
    if not api_products:
        print("⚠ Warning: No API products to map")
        return {}
    
    product_mapping = {}
    
    for product in api_products:
        product_id = product.get('id')
        
        if product_id is not None:
            product_mapping[product_id] = {
                'title': product.get('title'),
                'category': product.get('category'),
                'brand': product.get('brand'),
                'rating': product.get('rating')
            }
    
    print(f"✓ Created mapping for {len(product_mapping)} products")
    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()
    Returns: list of enriched transaction dictionaries
    
    Expected Output Format (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS ADDED FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True  # True if enrichment successful, False otherwise
    }
    
    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 → 101, P5 → 5)
    - If ID exists in product_mapping, add API fields
    - If ID doesn't exist, set API_Match to False and other fields to None
    - Handle all errors gracefully
    
    File Output:
    - Save enriched data to 'data/enriched_sales_data.txt'
    - Use same pipe-delimited format
    - Include new columns in header
    """
    
    if not transactions:
        print("⚠ Warning: No transactions to enrich")
        return []
    
    if not product_mapping:
        print("⚠ Warning: No product mapping available")
    
    print("\n" + "="*60)
    print("ENRICHING SALES DATA WITH API INFORMATION")
    print("="*60)
    
    enriched_transactions = []
    match_count = 0
    no_match_count = 0
    
    for trans in transactions:
        # Create enriched transaction with all original fields
        enriched_trans = trans.copy()
        
        try:
            # Extract numeric ID from ProductID (e.g., P101 → 101, P5 → 5)
            product_id_str = trans.get('ProductID', '')
            
            # Remove non-numeric characters to get ID
            numeric_match = re.search(r'\d+', product_id_str)
            
            if numeric_match:
                numeric_id = int(numeric_match.group())
                
                # Check if this ID exists in product mapping
                if numeric_id in product_mapping:
                    product_info = product_mapping[numeric_id]
                    
                    # Add API fields
                    enriched_trans['API_Category'] = product_info.get('category')
                    enriched_trans['API_Brand'] = product_info.get('brand')
                    enriched_trans['API_Rating'] = product_info.get('rating')
                    enriched_trans['API_Match'] = True
                    
                    match_count += 1
                else:
                    # No match found
                    enriched_trans['API_Category'] = None
                    enriched_trans['API_Brand'] = None
                    enriched_trans['API_Rating'] = None
                    enriched_trans['API_Match'] = False
                    
                    no_match_count += 1
            else:
                # Could not extract numeric ID
                enriched_trans['API_Category'] = None
                enriched_trans['API_Brand'] = None
                enriched_trans['API_Rating'] = None
                enriched_trans['API_Match'] = False
                
                no_match_count += 1
        
        except Exception as e:
            # Handle any errors gracefully
            print(f"⚠ Error enriching transaction {trans.get('TransactionID', 'Unknown')}: {e}")
            
            enriched_trans['API_Category'] = None
            enriched_trans['API_Brand'] = None
            enriched_trans['API_Rating'] = None
            enriched_trans['API_Match'] = False
            
            no_match_count += 1
        
        enriched_transactions.append(enriched_trans)
    
    # Print enrichment summary
    print(f"\nEnrichment Summary:")
    print(f"  Total transactions:     {len(transactions)}")
    print(f"  Successfully matched:   {match_count}")
    print(f"  No match found:         {no_match_count}")
    print(f"  Match rate:             {(match_count/len(transactions)*100):.1f}%")
    print("="*60)
    
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...
    
    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """
    
    if not enriched_transactions:
        print("⚠ Warning: No enriched transactions to save")
        return
    
    print("\n" + "="*60)
    print("SAVING ENRICHED DATA")
    print("="*60)
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Define column order
        columns = [
            'TransactionID', 'Date', 'ProductID', 'ProductName',
            'Quantity', 'UnitPrice', 'CustomerID', 'Region',
            'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
        ]
        
        # Open file for writing
        with open(filename, 'w', encoding='utf-8') as file:
            # Write header
            header = '|'.join(columns)
            file.write(header + '\n')
            
            # Write each transaction
            for trans in enriched_transactions:
                row_values = []
                
                for col in columns:
                    value = trans.get(col)
                    
                    # Handle None values
                    if value is None:
                        row_values.append('')
                    # Handle boolean values
                    elif isinstance(value, bool):
                        row_values.append(str(value))
                    # Handle numeric values
                    elif isinstance(value, (int, float)):
                        row_values.append(str(value))
                    # Handle string values
                    else:
                        row_values.append(str(value))
                
                row = '|'.join(row_values)
                file.write(row + '\n')
        
        print(f"✓ Successfully saved {len(enriched_transactions)} enriched transactions")
        print(f"✓ File location: {filename}")
        print("="*60)
        
    except Exception as e:
        print(f"✗ Error saving enriched data: {e}")
        print("="*60)
