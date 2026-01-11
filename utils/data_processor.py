"""
Data Processor Module
Handles analytical processing of sales transaction data
"""

from collections import defaultdict

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (total revenue)
    
    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    if not transactions:
        return 0.0
    
    total = 0.0
    for trans in transactions:
        quantity = trans.get('Quantity', 0)
        unit_price = trans.get('UnitPrice', 0.0)
        total += quantity * unit_price
    
    return round(total, 2)


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    Returns: dictionary with region statistics
    
    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }
    
    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """
    if not transactions:
        return {}
    
    # Calculate total revenue first (for percentages)
    total_revenue = calculate_total_revenue(transactions)
    
    # Aggregate by region
    region_data = defaultdict(lambda: {'total_sales': 0.0, 'transaction_count': 0})
    
    for trans in transactions:
        region = trans.get('Region', 'Unknown')
        quantity = trans.get('Quantity', 0)
        unit_price = trans.get('UnitPrice', 0.0)
        sales = quantity * unit_price
        
        region_data[region]['total_sales'] += sales
        region_data[region]['transaction_count'] += 1
    
    # Calculate percentages and format
    result = {}
    for region, data in region_data.items():
        percentage = (data['total_sales'] / total_revenue * 100) if total_revenue > 0 else 0.0
        result[region] = {
            'total_sales': round(data['total_sales'], 2),
            'transaction_count': data['transaction_count'],
            'percentage': round(percentage, 2)
        }
    
    # Sort by total_sales descending
    result = dict(sorted(result.items(), key=lambda x: x[1]['total_sales'], reverse=True))
    
    return result


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    Returns: list of tuples
    
    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]
    
    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """
    if not transactions:
        return []
    
    # Aggregate by product name
    product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
    
    for trans in transactions:
        product_name = trans.get('ProductName', 'Unknown')
        quantity = trans.get('Quantity', 0)
        unit_price = trans.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        product_data[product_name]['quantity'] += quantity
        product_data[product_name]['revenue'] += revenue
    
    # Convert to list of tuples
    product_list = [
        (product, data['quantity'], round(data['revenue'], 2))
        for product, data in product_data.items()
    ]
    
    # Sort by quantity descending
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    # Return top n
    return product_list[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    Returns: dictionary of customer statistics
    
    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }
    
    Requirements:
    - Calculate total amount spent per customer
    - Count number of purchases
    - Calculate average order value
    - List unique products bought
    - Sort by total_spent descending
    """
    if not transactions:
        return {}
    
    # Aggregate by customer
    customer_data = defaultdict(lambda: {
        'total_spent': 0.0,
        'purchase_count': 0,
        'products': set()
    })
    
    for trans in transactions:
        customer_id = trans.get('CustomerID', 'Unknown')
        quantity = trans.get('Quantity', 0)
        unit_price = trans.get('UnitPrice', 0.0)
        product_name = trans.get('ProductName', 'Unknown')
        
        amount_spent = quantity * unit_price
        
        customer_data[customer_id]['total_spent'] += amount_spent
        customer_data[customer_id]['purchase_count'] += 1
        customer_data[customer_id]['products'].add(product_name)
    
    # Format results
    result = {}
    for customer_id, data in customer_data.items():
        avg_order = data['total_spent'] / data['purchase_count'] if data['purchase_count'] > 0 else 0.0
        
        result[customer_id] = {
            'total_spent': round(data['total_spent'], 2),
            'purchase_count': data['purchase_count'],
            'avg_order_value': round(avg_order, 2),
            'products_bought': sorted(list(data['products']))  # Convert set to sorted list
        }
    
    # Sort by total_spent descending
    result = dict(sorted(result.items(), key=lambda x: x[1]['total_spent'], reverse=True))
    
    return result

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    Returns: dictionary sorted by date
    
    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }
    
    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """
    if not transactions:
        return {}
    
    # Aggregate by date
    daily_data = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0,
        'customers': set()
    })
    
    for trans in transactions:
        date = trans.get('Date', 'Unknown')
        quantity = trans.get('Quantity', 0)
        unit_price = trans.get('UnitPrice', 0.0)
        customer_id = trans.get('CustomerID', 'Unknown')
        
        revenue = quantity * unit_price
        
        daily_data[date]['revenue'] += revenue
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['customers'].add(customer_id)
    
    # Format results
    result = {}
    for date, data in daily_data.items():
        result[date] = {
            'revenue': round(data['revenue'], 2),
            'transaction_count': data['transaction_count'],
            'unique_customers': len(data['customers'])
        }
    
    # Sort chronologically by date
    result = dict(sorted(result.items()))
    
    return result


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    Returns: tuple (date, revenue, transaction_count)
    
    Expected Output Format:
    ('2024-12-15', 185000.0, 12)
    """
    if not transactions:
        return (None, 0.0, 0)
    
    # Get daily sales trend
    daily_trend = daily_sales_trend(transactions)
    
    if not daily_trend:
        return (None, 0.0, 0)
    
    # Find the date with maximum revenue
    peak_date = max(daily_trend.items(), key=lambda x: x[1]['revenue'])
    
    date = peak_date[0]
    revenue = peak_date[1]['revenue']
    transaction_count = peak_date[1]['transaction_count']
    
    return (date, revenue, transaction_count)


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    Returns: list of tuples
    
    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]
    
    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
    """
    if not transactions:
        return []
    
    # Aggregate by product name
    product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0.0})
    
    for trans in transactions:
        product_name = trans.get('ProductName', 'Unknown')
        quantity = trans.get('Quantity', 0)
        unit_price = trans.get('UnitPrice', 0.0)
        revenue = quantity * unit_price
        
        product_data[product_name]['quantity'] += quantity
        product_data[product_name]['revenue'] += revenue
    
    # Filter products with quantity < threshold
    low_performers = [
        (product, data['quantity'], round(data['revenue'], 2))
        for product, data in product_data.items()
        if data['quantity'] < threshold
    ]
    
    # Sort by quantity ascending (lowest first)
    low_performers.sort(key=lambda x: x[1])
    
    return low_performers


# Display helper functions
def display_daily_trend(daily_trend, show_all=False):
    """Display daily sales trend in formatted way"""
    print("\n" + "="*80)
    print("DAILY SALES TREND")
    print("="*80)
    print(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Customers':<12}")
    print("-"*80)
    
    # Show first 10 and last 5 if not show_all
    items = list(daily_trend.items())
    
    if not show_all and len(items) > 15:
        display_items = items[:10] + [('...', {'revenue': 0, 'transaction_count': 0, 'unique_customers': 0})] + items[-5:]
    else:
        display_items = items
    
    for date, stats in display_items:
        if date == '...':
            print("...")
            continue
        print(f"{date:<15} ₹{stats['revenue']:>15,.2f}  {stats['transaction_count']:<15} {stats['unique_customers']:<12}")
    
    # Summary
    total_revenue = sum(s['revenue'] for s in daily_trend.values())
    total_transactions = sum(s['transaction_count'] for s in daily_trend.values())
    avg_daily_revenue = total_revenue / len(daily_trend) if daily_trend else 0
    
    print("-"*80)
    print(f"{'SUMMARY:':<15}")
    print(f"  Total Days:        {len(daily_trend)}")
    print(f"  Total Revenue:     ₹{total_revenue:,.2f}")
    print(f"  Avg Daily Revenue: ₹{avg_daily_revenue:,.2f}")
    print(f"  Total Transactions: {total_transactions}")
    print("="*80)


def display_peak_day(peak_info):
    """Display peak sales day information"""
    date, revenue, count = peak_info
    
    print("\n" + "="*60)
    print("PEAK SALES DAY")
    print("="*60)
    
    if date is None:
        print("No data available")
    else:
        print(f"Date:                {date}")
        print(f"Revenue:             ₹{revenue:,.2f}")
        print(f"Transactions:        {count}")
        print(f"Avg per Transaction: ₹{revenue/count:,.2f}")
    
    print("="*60)


def display_low_performers(products, threshold):
    """Display low performing products"""
    print("\n" + "="*70)
    print(f"LOW PERFORMING PRODUCTS (Quantity < {threshold})")
    print("="*70)
    
    if not products:
        print("No low performing products found!")
    else:
        print(f"{'Product':<30} {'Quantity':<12} {'Revenue':<20}")
        print("-"*70)
        
        for product, qty, revenue in products:
            print(f"{product:<30} {qty:<12} ₹{revenue:>15,.2f}")
        
        print("-"*70)
        print(f"Total low performers: {len(products)}")
    
    print("="*70)


def generate_trend_report(transactions):
    """
    Generate trend analysis report
    """
    print("\n" + "="*80)
    print(" "*25 + "SALES TREND ANALYSIS")
    print("="*80)
    
    # 1. Daily Trend
    daily_trend = daily_sales_trend(transactions)
    display_daily_trend(daily_trend)
    
    # 2. Peak Sales Day
    peak_day = find_peak_sales_day(transactions)
    display_peak_day(peak_day)
    
    # 3. Low Performing Products
    low_products_10 = low_performing_products(transactions, threshold=10)
    display_low_performers(low_products_10, threshold=10)
    
    # 4. Additional Insights
    print("\n" + "="*60)
    print("TREND INSIGHTS")
    print("="*60)
    
    # Best and worst days
    if daily_trend:
        dates_sorted = sorted(daily_trend.items(), key=lambda x: x[1]['revenue'], reverse=True)
        best_day = dates_sorted[0]
        worst_day = dates_sorted[-1]
        
        print(f"\n📈 Best Day:   {best_day[0]} (₹{best_day[1]['revenue']:,.2f})")
        print(f"📉 Worst Day:  {worst_day[0]} (₹{worst_day[1]['revenue']:,.2f})")
        
        # Calculate growth/decline
        revenue_diff = best_day[1]['revenue'] - worst_day[1]['revenue']
        print(f"💰 Variance:   ₹{revenue_diff:,.2f}")
    
    # Product performance summary
    all_products = defaultdict(lambda: {'quantity': 0})
    for trans in transactions:
        product = trans.get('ProductName', 'Unknown')
        all_products[product]['quantity'] += trans.get('Quantity', 0)
    
    high_performers = sum(1 for p in all_products.values() if p['quantity'] >= 10)
    low_performers = len(low_products_10)
    
    print(f"\n📦 Products Analysis:")
    print(f"  High Performers (≥10 units): {high_performers}")
    print(f"  Low Performers (<10 units):  {low_performers}")
    print(f"  Total Products:              {len(all_products)}")
    
    print("="*60)

from datetime import datetime
import os

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    Report Must Include (in this order):
    1. HEADER
       - Report title
       - Generation date and time
       - Total records processed
    2. OVERALL SUMMARY
       - Total Revenue (formatted with commas)
       - Total Transactions
       - Average Order Value
       - Date Range of data
    3. REGION-WISE PERFORMANCE
       - Table showing each region with:
         * Total Sales Amount
         * Percentage of Total
         * Transaction Count
       - Sorted by sales amount descending
    4. TOP 5 PRODUCTS
       - Table with columns: Rank, Product Name, Quantity Sold, Revenue
    5. TOP 5 CUSTOMERS
       - Table with columns: Rank, Customer ID, Total Spent, Order Count
    6. DAILY SALES TREND
       - Table showing: Date, Revenue, Transactions, Unique Customers
    7. PRODUCT PERFORMANCE ANALYSIS
       - Best selling day
       - Low performing products (if any)
       - Average transaction value per region
    8. API ENRICHMENT SUMMARY
       - Total products enriched
       - Success rate percentage
       - List of products that couldn't be enriched
    """
    
    print("\n" + "="*80)
    print("GENERATING COMPREHENSIVE SALES REPORT")
    print("="*80)
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    try:
        # Calculate all required metrics
        total_revenue = calculate_total_revenue(transactions)
        region_stats = region_wise_sales(transactions)
        top_products = top_selling_products(transactions, n=5)
        customer_stats = customer_analysis(transactions)
        daily_trend = daily_sales_trend(transactions)
        peak_day = find_peak_sales_day(transactions)
        low_products = low_performing_products(transactions, threshold=10)
        
        # Get date range
        dates = sorted([t['Date'] for t in transactions if t.get('Date')])
        date_range_start = dates[0] if dates else 'N/A'
        date_range_end = dates[-1] if dates else 'N/A'
        
        # Enrichment statistics
        enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match'))
        total_enriched = len(enriched_transactions)
        enrichment_rate = (enriched_count / total_enriched * 100) if total_enriched > 0 else 0
        
        # Products that couldn't be enriched
        unenriched_products = set(
            t['ProductName'] 
            for t in enriched_transactions 
            if not t.get('API_Match')
        )
        
        # Open file for writing
        with open(output_file, 'w', encoding='utf-8') as f:
            
            # ========================================
            # 1. HEADER
            # ========================================
            f.write("="*80 + "\n")
            f.write(" "*25 + "SALES ANALYTICS REPORT\n")
            f.write(f" "*20 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f" "*23 + f"Records Processed: {len(transactions)}\n")
            f.write("="*80 + "\n\n")
            
            # ========================================
            # 2. OVERALL SUMMARY
            # ========================================
            f.write("OVERALL SUMMARY\n")
            f.write("-"*80 + "\n")
            f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
            f.write(f"Total Transactions:   {len(transactions)}\n")
            
            avg_order_value = total_revenue / len(transactions) if transactions else 0
            f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
            f.write(f"Date Range:           {date_range_start} to {date_range_end}\n")
            f.write("\n")
            
            # ========================================
            # 3. REGION-WISE PERFORMANCE
            # ========================================
            f.write("REGION-WISE PERFORMANCE\n")
            f.write("-"*80 + "\n")
            f.write(f"{'Region':<15} {'Sales':<20} {'% of Total':<15} {'Transactions':<15}\n")
            f.write("-"*80 + "\n")
            
            for region, stats in region_stats.items():
                f.write(f"{region:<15} ₹{stats['total_sales']:>15,.2f}  "
                       f"{stats['percentage']:>6.2f}%{' '*7} "
                       f"{stats['transaction_count']:<15}\n")
            
            f.write("\n")
            
            # ========================================
            # 4. TOP 5 PRODUCTS
            # ========================================
            f.write("TOP 5 PRODUCTS\n")
            f.write("-"*80 + "\n")
            f.write(f"{'Rank':<8} {'Product Name':<35} {'Quantity':<15} {'Revenue':<20}\n")
            f.write("-"*80 + "\n")
            
            for rank, (product, quantity, revenue) in enumerate(top_products, 1):
                f.write(f"{rank:<8} {product:<35} {quantity:<15} ₹{revenue:>15,.2f}\n")
            
            f.write("\n")
            
            # ========================================
            # 5. TOP 5 CUSTOMERS
            # ========================================
            f.write("TOP 5 CUSTOMERS\n")
            f.write("-"*80 + "\n")
            f.write(f"{'Rank':<8} {'Customer ID':<20} {'Total Spent':<20} {'Order Count':<15}\n")
            f.write("-"*80 + "\n")
            
            top_5_customers = list(customer_stats.items())[:5]
            for rank, (customer_id, stats) in enumerate(top_5_customers, 1):
                f.write(f"{rank:<8} {customer_id:<20} ₹{stats['total_spent']:>15,.2f}  "
                       f"{stats['purchase_count']:<15}\n")
            
            f.write("\n")
            
            # ========================================
            # 6. DAILY SALES TREND
            # ========================================
            f.write("DAILY SALES TREND\n")
            f.write("-"*80 + "\n")
            f.write(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<20}\n")
            f.write("-"*80 + "\n")
            
            # Show first 10 and last 5 days if more than 15 days
            daily_items = list(daily_trend.items())
            if len(daily_items) > 15:
                display_items = daily_items[:10] + [('...', None)] + daily_items[-5:]
            else:
                display_items = daily_items
            
            for date, stats in display_items:
                if date == '...':
                    f.write(f"{'...':<15} {'...':<20} {'...':<15} {'...':<20}\n")
                else:
                    f.write(f"{date:<15} ₹{stats['revenue']:>15,.2f}  "
                           f"{stats['transaction_count']:<15} "
                           f"{stats['unique_customers']:<20}\n")
            
            # Summary
            total_days = len(daily_trend)
            avg_daily_revenue = total_revenue / total_days if total_days > 0 else 0
            f.write("-"*80 + "\n")
            f.write(f"Total Days: {total_days}  |  Average Daily Revenue: ₹{avg_daily_revenue:,.2f}\n")
            f.write("\n")
            
            # ========================================
            # 7. PRODUCT PERFORMANCE ANALYSIS
            # ========================================
            f.write("PRODUCT PERFORMANCE ANALYSIS\n")
            f.write("-"*80 + "\n")
            
            # Best selling day
            peak_date, peak_revenue, peak_count = peak_day
            f.write(f"\nBest Selling Day:\n")
            f.write(f"  Date:         {peak_date}\n")
            f.write(f"  Revenue:      ₹{peak_revenue:,.2f}\n")
            f.write(f"  Transactions: {peak_count}\n")
            
            # Low performing products
            f.write(f"\nLow Performing Products (Quantity < 10):\n")
            if low_products:
                f.write(f"  {'Product':<30} {'Quantity':<12} {'Revenue':<15}\n")
                f.write("  " + "-"*60 + "\n")
                for product, qty, revenue in low_products[:10]:  # Show top 10
                    f.write(f"  {product:<30} {qty:<12} ₹{revenue:>12,.2f}\n")
                
                if len(low_products) > 10:
                    f.write(f"  ... and {len(low_products) - 10} more products\n")
            else:
                f.write("  No low performing products found.\n")
            
            # Average transaction value per region
            f.write(f"\nAverage Transaction Value by Region:\n")
            for region, stats in region_stats.items():
                avg_trans_value = stats['total_sales'] / stats['transaction_count'] if stats['transaction_count'] > 0 else 0
                f.write(f"  {region:<15} ₹{avg_trans_value:,.2f}\n")
            
            f.write("\n")
            
            # ========================================
            # 8. API ENRICHMENT SUMMARY
            # ========================================
            f.write("API ENRICHMENT SUMMARY\n")
            f.write("-"*80 + "\n")
            f.write(f"Total Products Enriched:     {enriched_count} out of {total_enriched}\n")
            f.write(f"Success Rate:                {enrichment_rate:.2f}%\n")
            
            f.write(f"\nProducts That Couldn't Be Enriched ({len(unenriched_products)}):\n")
            if unenriched_products:
                for i, product in enumerate(sorted(unenriched_products), 1):
                    f.write(f"  {i}. {product}\n")
                    if i >= 20:  # Limit to first 20
                        remaining = len(unenriched_products) - 20
                        if remaining > 0:
                            f.write(f"  ... and {remaining} more products\n")
                        break
            else:
                f.write("  All products successfully enriched!\n")
            
            f.write("\n")
            
            # ========================================
            # FOOTER
            # ========================================
            f.write("="*80 + "\n")
            f.write(" "*28 + "END OF REPORT\n")
            f.write("="*80 + "\n")
        
        print(f"✓ Report successfully generated: {output_file}")
        print(f"✓ Report size: {os.path.getsize(output_file)} bytes")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"✗ Error generating report: {e}")
        import traceback
        traceback.print_exc()
        print("="*80)
        return False
    
"""
Test script for report generation
"""

from utils.file_handler import read_sales_data
from utils.file_handler import parse_transactions, validate_and_filter
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from utils.data_processor import generate_sales_report

def main():
    print("="*80)
    print(" "*20 + "SALES REPORT GENERATION TEST")
    print("="*80)
    
    # Step 1: Load and prepare data
    print("\n[STEP 1] Loading sales data...")
    try:
        raw_lines = read_sales_data('data/sales_data.txt')
        transactions = parse_transactions(raw_lines)
        valid_trans, _, _ = validate_and_filter(transactions)
        print(f"✓ Loaded {len(valid_trans)} transactions")
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 2: Fetch API data and enrich
    print("\n[STEP 2] Fetching API data and enriching...")
    try:
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        enriched_trans = enrich_sales_data(valid_trans, product_mapping)
        print(f"✓ Enriched {len(enriched_trans)} transactions")
    except Exception as e:
        print(f"✗ Error: {e}")
        # Continue with un-enriched data
        enriched_trans = valid_trans
    
    # Step 3: Generate report
    print("\n[STEP 3] Generating comprehensive report...")
    success = generate_sales_report(
        transactions=valid_trans,
        enriched_transactions=enriched_trans,
        output_file='output/sales_report.txt'
    )
    
    if success:
        # Step 4: Display report preview
        print("\n[STEP 4] Report Preview (first 50 lines):")
        print("="*80)
        
        try:
            with open('output/sales_report.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines[:50], 1):
                print(line.rstrip())
            
            if len(lines) > 50:
                print(f"\n... ({len(lines) - 50} more lines)")
            
            print("\n" + "="*80)
            print(f"✓ Full report available at: output/sales_report.txt")
            print(f"✓ Total lines in report: {len(lines)}")
            
        except Exception as e:
            print(f"✗ Error reading report: {e}")
    else:
        print("✗ Report generation failed")
    
    print("\n" + "="*80)
    print(" "*25 + "TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
