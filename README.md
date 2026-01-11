This project involves creation of a Sales Analytics System using Python. 

End-to-end data pipeline for sales analysis with API integration and automated reporting.

## Features

- **ETL Pipeline**: Clean and validate messy sales data
- **API Integration**: Enrich data from DummyJSON API
- **Analytics**: Region-wise sales, customer segmentation, product performance
- **Reporting**: Auto-generated comprehensive sales reports

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the system
python main.py
```

## Input

Place `sales_data.txt` (pipe-delimited) in project root.

## Output

- `data/enriched_sales_data.txt` - API-enriched transactions
- `output/sales_report.txt` - Comprehensive analytics report

## Project Structure
```
SALES_ANALYTICS_SYSTEM/
├── utils/              # Core modules
│   ├── file_handler.py
│   ├── data_parser.py
│   ├── data_processor.py
│   └── api_handler.py
├── main.py             # Run this
└── sales_data.txt      # Your data here

## **Key Features:**

✅ **Progress tracking** with [X/10] steps  
✅ **User interaction** for filters  
✅ **Comprehensive error handling** at each step  
✅ **Graceful degradation** (continues without API if it fails)  
✅ **Clear visual separators** and formatting  
✅ **Summary at the end** with file locations  
✅ **Handles Ctrl+C** (KeyboardInterrupt)  
✅ **Detailed error messages** for debugging  
✅ **Validates user input** for filters  

## Tech Stack

Python • Requests • Pandas • DummyJSON API

## Author

V Aditi - BITS Pilani Business Analytics with GenAI Program