"""
Simple script to run preprocessing
Run this FIRST before using the NLP engine
"""

import os
import sys

print("\n" + "=" * 70)
print(" " * 20 + "DATA PREPROCESSING")
print("=" * 70)

# Check if input file exists
if not os.path.exists('customer_support_tickets.csv'):
    print("\n✗ ERROR: customer_support_tickets.csv not found!")
    print("\nPlease ensure the CSV file is in the current directory:")
    print(f"  Current directory: {os.getcwd()}")
    print("\nExpected file: customer_support_tickets.csv")
    sys.exit(1)

print("\n✓ Found customer_support_tickets.csv")
print("\nStarting preprocessing...\n")

# Import and run preprocessing
from preprocess_data import preprocess_tickets

try:
    df = preprocess_tickets(
        input_file='customer_support_tickets.csv',
        output_file='processed_tickets.csv'
    )
    
    if df is not None:
        print("\n" + "=" * 70)
        print("✓ SUCCESS! Preprocessing completed.")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Run: python test_nlp.py")
        print("   OR")
        print("2. Run: python nlp_engine.py")
        print("\n")
    else:
        print("\n✗ Preprocessing failed. Check error messages above.")
        
except Exception as e:
    print(f"\n✗ ERROR during preprocessing: {str(e)}")
    import traceback
    traceback.print_exc()
