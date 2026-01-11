"""
Sales Analytics System - Main Program
Orchestrates the entire data processing pipeline
"""

from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def print_separator(char='=', length=80):
    """Print a separator line"""
    print(char * length)

def print_step(step_num, total_steps, message):
    """Print a step in the process"""
    print(f"[{step_num}/{total_steps}] {message}")

def get_user_input(prompt, valid_options=None):
    """Get and validate user input"""
    while True:
        response = input(prompt).strip().lower()
        if valid_options is None or response in valid_options:
            return response
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}")

def display_filter_options(transactions):
    """Display available filter options to user"""
    print("\nFilter Options Available:")
    print("-" * 60)
    
    # Show available regions
    regions = sorted(set(t['Region'] for t in transactions if t.get('Region')))
    print(f"Regions: {', '.join(regions)}")
    
    # Show amount range
    amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
    if amounts:
        min_amount = min(amounts)
        max_amount = max(amounts)
        print(f"Amount Range: ₹{min_amount:,.2f} - ₹{max_amount:,.2f}")
    
    print("-" * 60)

def apply_filters(transactions):
    """Ask user for filter criteria and apply"""
    
    # Ask if user wants to filter
    want_filter = get_user_input("\nDo you want to filter data? (y/n): ", ['y', 'n'])
    
    if want_filter == 'n':
        print("✓ No filters applied")
        return transactions, None, None, None
    
    print("\nApplying Filters...")
    print("-" * 60)
    
    # Filter by region
    regions = sorted(set(t['Region'] for t in transactions if t.get('Region')))
    print(f"\nAvailable regions: {', '.join(regions)}")
    filter_region = input("Enter region to filter (or press Enter to skip): ").strip()
    
    if filter_region and filter_region not in regions:
        print(f"⚠ Warning: '{filter_region}' not found. Skipping region filter.")
        filter_region = None
    
    # Filter by amount
    filter_min = input("Enter minimum amount (or press Enter to skip): ").strip()
    filter_max = input("Enter maximum amount (or press Enter to skip): ").strip()
    
    min_amount = None
    max_amount = None
    
    try:
        if filter_min:
            min_amount = float(filter_min)
    except ValueError:
        print("⚠ Warning: Invalid minimum amount. Skipping min filter.")
    
    try:
        if filter_max:
            max_amount = float(filter_max)
    except ValueError:
        print("⚠ Warning: Invalid maximum amount. Skipping max filter.")
    
    return transactions, filter_region, min_amount, max_amount

def main():
    """
    Main execution function
    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses (call all functions from Part 2)
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations
    
    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors
    """
    
    TOTAL_STEPS = 10
    
    try:
        # ========================================
        # WELCOME MESSAGE
        # ========================================
        print_separator('=')
        print(" " * 25 + "SALES ANALYTICS SYSTEM")
        print_separator('=')
        print()
        
        # ========================================
        # STEP 1: READ SALES DATA
        # ========================================
        print_step(1, TOTAL_STEPS, "Reading sales data...")
        try:
            raw_lines = read_sales_data('data/sales_data.txt')
            print(f"✓ Successfully read {len(raw_lines)} transactions")
        except FileNotFoundError:
            print("✗ Error: sales_data.txt not found!")
            print("Please ensure sales_data.txt exists in the current directory.")
            return
        except Exception as e:
            print(f"✗ Error reading file: {e}")
            return
        
        # ========================================
        # STEP 2: PARSE AND CLEAN DATA
        # ========================================
        print_step(2, TOTAL_STEPS, "Parsing and cleaning data...")
        try:
            transactions = parse_transactions(raw_lines)
            print(f"✓ Parsed {len(transactions)} records")
        except Exception as e:
            print(f"✗ Error parsing data: {e}")
            return
        
        if not transactions:
            print("✗ Error: No valid transactions found!")
            return
        
        # ========================================
        # STEP 3: DISPLAY FILTER OPTIONS
        # ========================================
        print_step(3, TOTAL_STEPS, "Filter Options")
        try:
            display_filter_options(transactions)
            transactions_to_process, filter_region, min_amount, max_amount = apply_filters(transactions)
        except Exception as e:
            print(f"⚠ Warning: Error with filters: {e}")
            print("Continuing without filters...")
            transactions_to_process = transactions
            filter_region = None
            min_amount = None
            max_amount = None
        
        # ========================================
        # STEP 4: VALIDATE TRANSACTIONS
        # ========================================
        print_step(4, TOTAL_STEPS, "Validating transactions...")
        try:
            valid_trans, invalid_count, filter_summary = validate_and_filter(
                transactions_to_process,
                region=filter_region,
                min_amount=min_amount,
                max_amount=max_amount
            )
            
            valid_count = len(valid_trans)
            print(f"✓ Valid: {valid_count} | Invalid: {invalid_count}")
            
            if filter_region or min_amount or max_amount:
                print(f"✓ After filters: {filter_summary['final_count']} transactions")
        
        except Exception as e:
            print(f"✗ Error validating data: {e}")
            return
        
        if not valid_trans:
            print("✗ Error: No valid transactions after validation!")
            return
        
        # ========================================
        # STEP 5: ANALYZE SALES DATA
        # ========================================
        print_step(5, TOTAL_STEPS, "Analyzing sales data...")
        try:
            # Calculate all metrics
            total_revenue = calculate_total_revenue(valid_trans)
            region_stats = region_wise_sales(valid_trans)
            top_products = top_selling_products(valid_trans, n=5)
            customer_stats = customer_analysis(valid_trans)
            daily_trend = daily_sales_trend(valid_trans)
            peak_day = find_peak_sales_day(valid_trans)
            low_products = low_performing_products(valid_trans, threshold=10)
            
            print(f"✓ Analysis complete")
            print(f"  Total Revenue: ₹{total_revenue:,.2f}")
            print(f"  Regions Analyzed: {len(region_stats)}")
            print(f"  Top Products Identified: {len(top_products)}")
            print(f"  Customers Analyzed: {len(customer_stats)}")
            
        except Exception as e:
            print(f"⚠ Warning: Error in analysis: {e}")
            print("Some analyses may be incomplete...")
        
        # ========================================
        # STEP 6: FETCH PRODUCT DATA FROM API
        # ========================================
        print_step(6, TOTAL_STEPS, "Fetching product data from API...")
        try:
            api_products = fetch_all_products()
            
            if api_products:
                print(f"✓ Fetched {len(api_products)} products")
            else:
                print("⚠ Warning: Could not fetch API products")
                print("Continuing without API enrichment...")
                api_products = []
        
        except Exception as e:
            print(f"⚠ Warning: API fetch error: {e}")
            print("Continuing without API enrichment...")
            api_products = []
        
        # ========================================
        # STEP 7: ENRICH SALES DATA
        # ========================================
        print_step(7, TOTAL_STEPS, "Enriching sales data...")
        
        if api_products:
            try:
                product_mapping = create_product_mapping(api_products)
                enriched_trans = enrich_sales_data(valid_trans, product_mapping)
                
                enriched_count = sum(1 for t in enriched_trans if t.get('API_Match'))
                total_trans = len(enriched_trans)
                success_rate = (enriched_count / total_trans * 100) if total_trans > 0 else 0
                
                print(f"✓ Enriched {enriched_count}/{total_trans} transactions ({success_rate:.1f}%)")
            
            except Exception as e:
                print(f"⚠ Warning: Enrichment error: {e}")
                enriched_trans = valid_trans
                print("Using non-enriched data...")
        else:
            enriched_trans = valid_trans
            print("⚠ Skipping enrichment (no API data)")
        
        # ========================================
        # STEP 8: SAVE ENRICHED DATA
        # ========================================
        print_step(8, TOTAL_STEPS, "Saving enriched data...")
        try:
            save_enriched_data(enriched_trans, filename='data/enriched_sales_data.txt')
            print(f"✓ Saved to: data/enriched_sales_data.txt")
        except Exception as e:
            print(f"⚠ Warning: Could not save enriched data: {e}")
        
        # ========================================
        # STEP 9: GENERATE REPORT
        # ========================================
        print_step(9, TOTAL_STEPS, "Generating comprehensive report...")
        try:
            success = generate_sales_report(
                transactions=valid_trans,
                enriched_transactions=enriched_trans,
                output_file='output/sales_report.txt'
            )
            
            if success:
                print(f"✓ Report saved to: output/sales_report.txt")
            else:
                print(f"⚠ Warning: Report generation had issues")
        
        except Exception as e:
            print(f"⚠ Warning: Report generation error: {e}")
        
        # ========================================
        # STEP 10: COMPLETION
        # ========================================
        print_step(10, TOTAL_STEPS, "Process Complete!")
        print_separator('=')
        
        print("\n📊 SUMMARY:")
        print(f"  Transactions Processed: {len(valid_trans)}")
        print(f"  Total Revenue: ₹{total_revenue:,.2f}")
        print(f"  Files Generated:")
        print(f"    • data/enriched_sales_data.txt")
        print(f"    • output/sales_report.txt")
        
        print("\n✨ Success! All processes completed.")
        print_separator('=')
        
    except KeyboardInterrupt:
        print("\n\n⚠ Process interrupted by user.")
        print("Exiting...")
    
    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {e}")
        print("\nPlease check:")
        print("  1. sales_data.txt exists")
        print("  2. All required modules are installed (requests, pandas)")
        print("  3. Internet connection (for API calls)")
        print("\nFor detailed error information, check the console output above.")
        
        import traceback
        print("\n" + "="*80)
        print("TECHNICAL ERROR DETAILS:")
        print("="*80)
        traceback.print_exc()

if __name__ == "__main__":
    main()
