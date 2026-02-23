"""
Data Preprocessing Script for IT Ticket Resolution System
Processes CSV with columns: Ticket Type, Ticket Subject, Ticket Description, Resolution, Ticket Priority
"""

import pandas as pd
import re
import numpy as np

def clean_text(text):
    """Clean and preprocess text data"""
    if pd.isna(text) or text == '':
        return ''
    
    text = str(text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove product placeholders
    text = re.sub(r'\{product_purchased\}', 'product', text)
    text = re.sub(r'\{product_\w+\}', 'product', text)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    
    # Remove phone numbers
    text = re.sub(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', '', text)
    text = re.sub(r'\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}', '', text)
    
    # Remove zip codes
    text = re.sub(r'\b\d{5}(-\d{4})?\b', '', text)
    
    # Remove special characters but keep spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove standalone numbers
    text = re.sub(r'\b\d+\b', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def preprocess_tickets(input_file='customer_support_tickets.csv', output_file='processed_tickets.csv'):
    """
    Preprocess ticket data - keep only required columns and clean data
    """
    print("=" * 60)
    print("IT TICKET DATA PREPROCESSING")
    print("=" * 60)
    
    # Read CSV
    print(f"\n[1/5] Reading data from: {input_file}")
    df = pd.read_csv(input_file)
    print(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Select required columns
    print("\n[2/5] Selecting required columns...")
    required_columns = [
        'Ticket Type',
        'Ticket Subject',
        'Ticket Description',
        'Resolution',
        'Ticket Priority'
    ]
    
    # Check if columns exist
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        print(f"   ✗ ERROR: Missing columns: {missing_cols}")
        print(f"   Available columns: {df.columns.tolist()}")
        return None
    
    df_processed = df[required_columns].copy()
    print(f"   ✓ Selected {len(required_columns)} columns")
    
    # Filter rows with valid resolutions
    print("\n[3/5] Filtering data...")
    print(f"   Initial rows: {len(df_processed)}")
    
    # Remove rows with missing Resolution
    df_processed = df_processed[df_processed['Resolution'].notna()]
    print(f"   After removing null resolutions: {len(df_processed)}")
    
    # Remove rows with empty Resolution
    df_processed = df_processed[df_processed['Resolution'].str.strip() != '']
    print(f"   After removing empty resolutions: {len(df_processed)}")
    
    # Remove rows with missing descriptions
    df_processed = df_processed[df_processed['Ticket Description'].notna()]
    print(f"   After removing null descriptions: {len(df_processed)}")
    
    # Clean text data
    print("\n[4/5] Cleaning text data...")
    df_processed['Ticket Type'] = df_processed['Ticket Type'].apply(clean_text)
    df_processed['Ticket Subject'] = df_processed['Ticket Subject'].apply(clean_text)
    df_processed['Ticket Description'] = df_processed['Ticket Description'].apply(clean_text)
    df_processed['Resolution'] = df_processed['Resolution'].apply(clean_text)
    print("   ✓ Text cleaning completed")
    
    # Remove duplicates
    initial_count = len(df_processed)
    df_processed = df_processed.drop_duplicates(subset=['Ticket Description', 'Resolution'])
    print(f"   ✓ Removed {initial_count - len(df_processed)} duplicate entries")
    
    # Save processed data
    print(f"\n[5/5] Saving processed data to: {output_file}")
    df_processed.to_csv(output_file, index=False)
    print(f"   ✓ Saved {len(df_processed)} processed tickets")
    
    # Display statistics
    print("\n" + "=" * 60)
    print("DATA STATISTICS")
    print("=" * 60)
    print(f"\nTotal Tickets: {len(df_processed)}")
    
    print("\nTicket Type Distribution:")
    type_counts = df_processed['Ticket Type'].value_counts()
    for ticket_type, count in type_counts.head(10).items():
        print(f"  • {ticket_type}: {count}")
    
    print("\nPriority Distribution:")
    priority_counts = df_processed['Ticket Priority'].value_counts()
    for priority, count in priority_counts.items():
        print(f"  • {priority}: {count}")
    
    print("\nSample Data:")
    print(df_processed.head(3).to_string())
    
    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETE!")
    print("=" * 60)
    
    return df_processed

if __name__ == "__main__":
    preprocess_tickets()
