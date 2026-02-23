"""
Master Run Script - Automatically handles setup and execution
"""

import os
import sys

def check_file(filename):
    """Check if file exists"""
    return os.path.exists(filename)

def main():
    print("\n" + "=" * 70)
    print(" " * 15 + "IT TICKET NLP ENGINE - SETUP CHECK")
    print("=" * 70)
    
    # Check original dataset
    print("\n[1/3] Checking for original dataset...")
    if not check_file('customer_support_tickets.csv'):
        print("  ✗ customer_support_tickets.csv NOT FOUND")
        print("\n  Please place your CSV file in this directory:")
        print(f"  {os.getcwd()}")
        sys.exit(1)
    else:
        print("  ✓ customer_support_tickets.csv found")
    
    # Check if preprocessing is needed
    print("\n[2/3] Checking for preprocessed data...")
    if not check_file('processed_tickets.csv'):
        print("  ✗ processed_tickets.csv NOT FOUND")
        print("  → Running preprocessing now...\n")
        
        try:
            from preprocess_data import preprocess_tickets
            df = preprocess_tickets(
                input_file='customer_support_tickets.csv',
                output_file='processed_tickets.csv'
            )
            
            if df is None:
                print("\n  ✗ Preprocessing failed!")
                sys.exit(1)
            
            print("\n  ✓ Preprocessing completed successfully!")
            
        except Exception as e:
            print(f"\n  ✗ Error during preprocessing: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        print("  ✓ processed_tickets.csv found")
    
    # Run NLP engine demo
    print("\n[3/3] Running NLP Engine Demo...")
    print("-" * 70)
    
    try:
        from nlp_engine import TicketNLPEngine
        
        engine = TicketNLPEngine()
        engine.load_data('processed_tickets.csv')
        
        stats = engine.get_statistics()
        print("\n✓ NLP Engine loaded successfully!")
        print(f"  Total tickets: {stats['total_tickets']}")
        print(f"  Vocabulary size: {stats['vocabulary_size']}")
        
        # Run a quick test
        print("\n" + "=" * 70)
        print("QUICK TEST: Network Problem")
        print("=" * 70)
        
        similar = engine.find_similar_tickets(
            ticket_type="technical issue",
            subject="network problem",
            description="cannot connect to wifi internet not working",
            top_k=3
        )
        
        if similar:
            print(f"\n✓ Found {len(similar)} similar tickets!")
            print("\nTop recommendation:")
            print(f"  Similarity: {similar[0]['similarity_score']:.1%}")
            print(f"  Resolution: {similar[0]['resolution'][:100]}...")
        else:
            print("\n⚠ No similar tickets found (this is unusual)")
        
        print("\n" + "=" * 70)
        print("✓ ALL CHECKS PASSED!")
        print("=" * 70)
        print("\nYou can now:")
        print("  1. Run interactive tests: python test_nlp.py")
        print("  2. Use the engine in your code (see README.md)")
        print("  3. Run full demo: python nlp_engine.py")
        print("\n")
        
    except Exception as e:
        print(f"\n✗ Error running NLP engine: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
