"""
Test script for data enrichment functions
"""

from file_handler import read_sales_data
from file_handler import parse_transactions, validate_and_filter
from api_handler import fetch_all_products

from api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)

def main():
    print("="*80)
    print(" "*20 + "DATA ENRICHMENT TEST")
    print("="*80)
    
    # Step 1: Load sales data
    print("\n[STEP 1] Loading sales data...")
    try:
        raw_lines = read_sales_data('data/sales_data.txt')
        transactions = parse_transactions(raw_lines)
        valid_trans, _, _ = validate_and_filter(transactions)
        
        print(f"✓ Loaded {len(valid_trans)} valid transactions")
        
    except Exception as e:
        print(f"✗ Error loading sales data: {e}")
        return
    
    # Step 2: Fetch API products
    print("\n" + "="*80)
    print("\n[STEP 2] Fetching products from API...")
    api_products = fetch_all_products()
    
    if not api_products:
        print("✗ Failed to fetch API products")
        return
    
    # Step 3: Create product mapping
    print("\n" + "="*80)
    print("\n[STEP 3] Creating product mapping...")
    product_mapping = create_product_mapping(api_products)
    
    print(f"\nSample mapping (first 5 products):")
    for product_id, info in list(product_mapping.items())[:5]:
        print(f"  ID {product_id}: {info['title']} ({info['category']}) - {info['brand']}")
    
    # Step 4: Enrich sales data
    print("\n" + "="*80)
    print("\n[STEP 4] Enriching sales data...")
    enriched_trans = enrich_sales_data(valid_trans, product_mapping)
    
    # Show sample enriched transactions
    print("\nSample enriched transactions:")
    print("-"*80)
    
    for i, trans in enumerate(enriched_trans[:3], 1):
        print(f"\n{i}. Transaction {trans['TransactionID']}:")
        print(f"   Original:")
        print(f"     Product: {trans['ProductName']} ({trans['ProductID']})")
        print(f"     Quantity: {trans['Quantity']} x ₹{trans['UnitPrice']:,.2f}")
        print(f"   Enriched:")
        if trans['API_Match']:
            print(f"     API Category: {trans['API_Category']}")
            print(f"     API Brand: {trans['API_Brand']}")
            print(f"     API Rating: {trans['API_Rating']}/5.0")
            print(f"     ✓ Match found")
        else:
            print(f"     ✗ No API match")
    
    # Step 5: Save enriched data
    print("\n" + "="*80)
    print("\n[STEP 5] Saving enriched data to file...")
    save_enriched_data(enriched_trans, filename='data/enriched_sales_data.txt')
    
    # Step 6: Verify saved file
    print("\n" + "="*80)
    print("\n[STEP 6] Verifying saved file...")
    
    try:
        with open('data/enriched_sales_data.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"✓ File contains {len(lines)} lines (including header)")
        print(f"\nHeader:")
        print(f"  {lines[0].strip()}")
        print(f"\nFirst data row:")
        print(f"  {lines[1].strip()}")
        
    except Exception as e:
        print(f"✗ Error verifying file: {e}")
    
    # Step 7: Analysis of enrichment
    print("\n" + "="*80)
    print("\n[STEP 7] Enrichment Analysis")
    print("="*80)
    
    matched = sum(1 for t in enriched_trans if t.get('API_Match'))
    unmatched = len(enriched_trans) - matched
    
    # Count by category (for matched transactions)
    from collections import Counter
    categories = Counter(
        t['API_Category'] 
        for t in enriched_trans 
        if t.get('API_Match') and t.get('API_Category')
    )
    
    brands = Counter(
        t['API_Brand'] 
        for t in enriched_trans 
        if t.get('API_Match') and t.get('API_Brand')
    )
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total transactions:    {len(enriched_trans)}")
    print(f"  API matched:           {matched} ({matched/len(enriched_trans)*100:.1f}%)")
    print(f"  Not matched:           {unmatched} ({unmatched/len(enriched_trans)*100:.1f}%)")
    
    if categories:
        print(f"\n📦 Top 5 Categories (from API):")
        for cat, count in categories.most_common(5):
            print(f"  {cat}: {count} transactions")
    
    if brands:
        print(f"\n🏢 Top 5 Brands (from API):")
        for brand, count in brands.most_common(5):
            print(f"  {brand}: {count} transactions")
    
    # Average rating for matched products
    ratings = [
        t['API_Rating'] 
        for t in enriched_trans 
        if t.get('API_Match') and t.get('API_Rating') is not None
    ]
    
    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        print(f"\n⭐ Average Product Rating: {avg_rating:.2f}/5.0")
    
    print("\n" + "="*80)
    print(" "*25 + "ENRICHMENT COMPLETE ✓")
    print("="*80)

if __name__ == "__main__":
    main()