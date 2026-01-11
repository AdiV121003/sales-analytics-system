"""
File Handler Module
Handles reading sales data with encoding issues
"""

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    
    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    
    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    
    # List of encodings to try in order
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    lines = []
    successful_encoding = None
    
    # Try to read file with different encodings
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding, errors='strict') as file:
                # Read all lines
                all_lines = file.readlines()
                
                # Skip header (first line) and process rest
                for line in all_lines[1:]:
                    # Strip whitespace
                    line = line.strip()
                    
                    # Skip empty lines
                    if line:
                        lines.append(line)
                
                successful_encoding = encoding
                print(f"✓ Successfully read file using '{encoding}' encoding")
                print(f"✓ Total lines read: {len(lines)}")
                break  # Successfully read, exit loop
                
        except FileNotFoundError:
            # File doesn't exist - raise error immediately
            raise FileNotFoundError(f"Error: File '{filename}' not found. Please check the file path.")
        
        except UnicodeDecodeError:
            # This encoding didn't work, try next one
            print(f"✗ Failed to read with '{encoding}' encoding, trying next...")
            continue
        
        except Exception as e:
            # Other unexpected errors
            print(f"✗ Unexpected error with '{encoding}' encoding: {e}")
            continue
    
    # If no encoding worked
    if not successful_encoding:
        raise ValueError(f"Error: Could not read file '{filename}' with any supported encoding (tried: {', '.join(encodings)})")
    
    # Validate we got data
    if not lines:
        raise ValueError(f"Error: File '{filename}' is empty or contains only header")
    
    return lines


def validate_line_format(line):
    """
    Validates if a line has correct pipe-delimited format
    Returns: True if valid, False otherwise
    
    Expected format: field1|field2|field3|field4|field5|field6|field7|field8
    (8 fields separated by pipes)
    """
    fields = line.split('|')
    return len(fields) == 8


def get_file_statistics(lines):
    """
    Get statistics about the file content
    Returns: dictionary with statistics
    """
    stats = {
        'total_lines': len(lines),
        'valid_format': 0,
        'invalid_format': 0
    }
    
    for line in lines:
        if validate_line_format(line):
            stats['valid_format'] += 1
        else:
            stats['invalid_format'] += 1
    
    return stats


# Test function
if __name__ == "__main__":
    """
    Test the file reading functionality
    """
    print("="*60)
    print("TESTING FILE HANDLER")
    print("="*60)
    
    # Test 1: Read existing file
    try:
        print("\nTest 1: Reading sales_data.txt")
        print("-"*60)
        lines = read_sales_data('data/sales_data.txt')
        
        print(f"\n✓ Successfully read {len(lines)} lines")
        
        # Show first 5 lines
        print("\nFirst 5 lines:")
        for i, line in enumerate(lines[:5], 1):
            print(f"  {i}. {line}")
        
        # Get statistics
        stats = get_file_statistics(lines)
        print("\nFile Statistics:")
        print(f"  Total lines: {stats['total_lines']}")
        print(f"  Valid format (8 fields): {stats['valid_format']}")
        print(f"  Invalid format: {stats['invalid_format']}")
        
    except FileNotFoundError as e:
        print(f"\n✗ {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
    
    # Test 2: Try non-existent file
    print("\n" + "="*60)
    print("\nTest 2: Reading non-existent file")
    print("-"*60)
    try:
        lines = read_sales_data('nonexistent_file.txt')
    except FileNotFoundError as e:
        print(f"✓ Correctly caught error: {e}")
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)

"""
Data Parser Module
Handles parsing and validation of sales transaction data
"""

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]
    
    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    
    transactions = []
    skipped_count = 0
    
    print("\n" + "="*60)
    print("PARSING TRANSACTIONS")
    print("="*60)
    
    for line_num, line in enumerate(raw_lines, start=1):
        try:
            # Split by pipe delimiter
            fields = line.split('|')
            
            # Check if we have correct number of fields (8 expected)
            if len(fields) != 8:
                print(f"Line {line_num}: Skipped (incorrect field count: {len(fields)} fields)")
                skipped_count += 1
                continue
            
            # Extract and clean fields
            transaction_id = fields[0].strip()
            date = fields[1].strip()
            product_id = fields[2].strip()
            product_name = fields[3].strip()
            quantity_str = fields[4].strip()
            unit_price_str = fields[5].strip()
            customer_id = fields[6].strip()
            region = fields[7].strip()
            
            # Clean ProductName: remove commas (replace with space)
            product_name_clean = product_name.replace(',', ' ')
            
            # Clean numeric fields: remove commas and convert types
            try:
                quantity_clean = quantity_str.replace(',', '')
                quantity = int(quantity_clean)
            except ValueError:
                print(f"Line {line_num}: Skipped (invalid Quantity: '{quantity_str}')")
                skipped_count += 1
                continue
            
            try:
                unit_price_clean = unit_price_str.replace(',', '')
                unit_price = float(unit_price_clean)
            except ValueError:
                print(f"Line {line_num}: Skipped (invalid UnitPrice: '{unit_price_str}')")
                skipped_count += 1
                continue
            
            # Create transaction dictionary
            transaction = {
                'TransactionID': transaction_id,
                'Date': date,
                'ProductID': product_id,
                'ProductName': product_name_clean,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Region': region
            }
            
            transactions.append(transaction)
            
        except Exception as e:
            print(f"Line {line_num}: Skipped (parsing error: {e})")
            skipped_count += 1
            continue
    
    print(f"\n✓ Successfully parsed: {len(transactions)} transactions")
    print(f"✗ Skipped: {skipped_count} lines")
    print("="*60)
    
    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    
    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)
    
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    
    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )
    
    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'
    
    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """
    
    print("\n" + "="*60)
    print("VALIDATION AND FILTERING")
    print("="*60)
    
    total_input = len(transactions)
    print(f"\nTotal input transactions: {total_input}")
    
    # Step 1: Validation
    print("\n--- STEP 1: VALIDATION ---")
    valid_transactions = []
    invalid_count = 0
    
    for trans in transactions:
        is_valid = True
        reasons = []
        
        # Rule 1: All required fields must be present (not empty)
        required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                          'Quantity', 'UnitPrice', 'CustomerID', 'Region']
        for field in required_fields:
            if field not in trans or not str(trans[field]).strip():
                is_valid = False
                reasons.append(f"Missing {field}")
        
        # Rule 2: Quantity must be > 0
        if trans.get('Quantity', 0) <= 0:
            is_valid = False
            reasons.append(f"Invalid Quantity ({trans.get('Quantity')})")
        
        # Rule 3: UnitPrice must be > 0
        if trans.get('UnitPrice', 0) <= 0:
            is_valid = False
            reasons.append(f"Invalid UnitPrice ({trans.get('UnitPrice')})")
        
        # Rule 4: TransactionID must start with 'T'
        if not str(trans.get('TransactionID', '')).startswith('T'):
            is_valid = False
            reasons.append(f"Invalid TransactionID format ({trans.get('TransactionID')})")
        
        # Rule 5: ProductID must start with 'P'
        if not str(trans.get('ProductID', '')).startswith('P'):
            is_valid = False
            reasons.append(f"Invalid ProductID format ({trans.get('ProductID')})")
        
        # Rule 6: CustomerID must start with 'C'
        if not str(trans.get('CustomerID', '')).startswith('C'):
            is_valid = False
            reasons.append(f"Invalid CustomerID format ({trans.get('CustomerID')})")
        
        if is_valid:
            valid_transactions.append(trans)
        else:
            invalid_count += 1
            if invalid_count <= 5:  # Show first 5 invalid records
                print(f"  Invalid: {trans.get('TransactionID', 'N/A')} - {', '.join(reasons)}")
    
    if invalid_count > 5:
        print(f"  ... and {invalid_count - 5} more invalid records")
    
    print(f"\n✓ Valid transactions: {len(valid_transactions)}")
    print(f"✗ Invalid transactions: {invalid_count}")
    
    # Calculate transaction amounts
    for trans in valid_transactions:
        trans['Amount'] = trans['Quantity'] * trans['UnitPrice']
    
    # Display available data insights
    print("\n--- DATA INSIGHTS ---")
    
    # Show available regions
    regions = sorted(set(trans['Region'] for trans in valid_transactions))
    print(f"Available regions: {', '.join(regions)}")
    
    # Show amount range
    amounts = [trans['Amount'] for trans in valid_transactions]
    if amounts:
        min_total = min(amounts)
        max_total = max(amounts)
        avg_total = sum(amounts) / len(amounts)
        print(f"Transaction amount range: ₹{min_total:,.2f} - ₹{max_total:,.2f}")
        print(f"Average transaction amount: ₹{avg_total:,.2f}")
    
    # Step 2: Apply Filters
    filtered_transactions = valid_transactions.copy()
    filtered_by_region = 0
    filtered_by_amount = 0
    
    # Filter by Region
    if region:
        print(f"\n--- STEP 2: FILTERING BY REGION ---")
        print(f"Filter: Region = '{region}'")
        before_count = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]
        after_count = len(filtered_transactions)
        filtered_by_region = before_count - after_count
        print(f"Records after region filter: {after_count} (removed {filtered_by_region})")
    
    # Filter by Amount Range
    if min_amount is not None or max_amount is not None:
        print(f"\n--- STEP 3: FILTERING BY AMOUNT ---")
        before_count = len(filtered_transactions)
        
        if min_amount is not None:
            print(f"Filter: Amount >= ₹{min_amount:,.2f}")
            filtered_transactions = [t for t in filtered_transactions if t['Amount'] >= min_amount]
        
        if max_amount is not None:
            print(f"Filter: Amount <= ₹{max_amount:,.2f}")
            filtered_transactions = [t for t in filtered_transactions if t['Amount'] <= max_amount]
        
        after_count = len(filtered_transactions)
        filtered_by_amount = before_count - after_count
        print(f"Records after amount filter: {after_count} (removed {filtered_by_amount})")
    
    # Create summary
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }
    
    print("\n" + "="*60)
    print("FILTERING SUMMARY")
    print("="*60)
    print(f"Total input:           {filter_summary['total_input']}")
    print(f"Invalid removed:       {filter_summary['invalid']}")
    print(f"Filtered by region:    {filter_summary['filtered_by_region']}")
    print(f"Filtered by amount:    {filter_summary['filtered_by_amount']}")
    print(f"Final valid count:     {filter_summary['final_count']}")
    print("="*60)
    
    return filtered_transactions, invalid_count, filter_summary


# Helper function for testing
def display_sample_transactions(transactions, count=5):
    """
    Display sample transactions in a readable format
    """
    print(f"\nSample Transactions (showing {min(count, len(transactions))} of {len(transactions)}):")
    print("-"*60)
    
    for i, trans in enumerate(transactions[:count], 1):
        print(f"\n{i}. Transaction: {trans['TransactionID']}")
        print(f"   Date: {trans['Date']}")
        print(f"   Product: {trans['ProductName']} ({trans['ProductID']})")
        print(f"   Quantity: {trans['Quantity']} x ₹{trans['UnitPrice']:,.2f}")
        if 'Amount' in trans:
            print(f"   Total: ₹{trans['Amount']:,.2f}")
        print(f"   Customer: {trans['CustomerID']} | Region: {trans['Region']}")


# Test functions
if __name__ == "__main__":
    """
    Test the parsing and validation functions
    """
    from file_handler import read_sales_data
    
    print("="*60)
    print("TESTING DATA PARSER MODULE")
    print("="*60)
    
    # Test 1: Parse transactions
    try:
        print("\nTest 1: Parsing sales_data.txt")
        raw_lines = read_sales_data('data/sales_data.txt')
        transactions = parse_transactions(raw_lines)
        
        # Display samples
        display_sample_transactions(transactions, 3)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        transactions = []
    
    # Test 2: Validate without filters
    if transactions:
        print("\n" + "="*60)
        print("\nTest 2: Validation (no filters)")
        valid, invalid_count, summary = validate_and_filter(transactions)
        display_sample_transactions(valid, 3)
    
    # Test 3: Validate with region filter
    if transactions:
        print("\n" + "="*60)
        print("\nTest 3: Validation with Region filter")
        valid, invalid_count, summary = validate_and_filter(
            transactions, 
            region='North'
        )
        display_sample_transactions(valid, 3)
    
    # Test 4: Validate with amount filter
    if transactions:
        print("\n" + "="*60)
        print("\nTest 4: Validation with Amount filter")
        valid, invalid_count, summary = validate_and_filter(
            transactions,
            min_amount=10000,
            max_amount=50000
        )
        display_sample_transactions(valid, 3)
    
    # Test 5: Validate with all filters
    if transactions:
        print("\n" + "="*60)
        print("\nTest 5: Validation with ALL filters")
        valid, invalid_count, summary = validate_and_filter(
            transactions,
            region='South',
            min_amount=5000,
            max_amount=30000
        )
        display_sample_transactions(valid, 3)
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETE")
    print("="*60)