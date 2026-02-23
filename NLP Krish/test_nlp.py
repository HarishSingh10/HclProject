"""
Interactive Test Script for NLP Engine
Allows testing the ticket resolution recommendation system
"""

from nlp_engine import TicketNLPEngine

def test_interactive():
    """
    Interactive testing interface
    """
    print("\n" + "=" * 70)
    print(" " * 15 + "IT TICKET RESOLUTION NLP ENGINE")
    print("=" * 70)
    
    # Initialize and load engine
    print("\nInitializing NLP Engine...")
    engine = TicketNLPEngine()
    
    try:
        engine.load_data('processed_tickets.csv')
    except FileNotFoundError:
        print("\n✗ ERROR: processed_tickets.csv not found!")
        print("Please run: python preprocess_data.py first")
        return
    
    # Show statistics
    stats = engine.get_statistics()
    print("\n" + "-" * 70)
    print("ENGINE STATISTICS")
    print("-" * 70)
    print(f"Total Historical Tickets: {stats['total_tickets']}")
    print(f"Vocabulary Size: {stats['vocabulary_size']}")
    print(f"\nTicket Types Available:")
    for ticket_type, count in list(stats['ticket_types'].items())[:5]:
        print(f"  • {ticket_type}: {count}")
    
    # Interactive loop
    while True:
        print("\n" + "=" * 70)
        print("TEST NEW TICKET")
        print("=" * 70)
        
        print("\nEnter ticket details (or 'quit' to exit):")
        
        ticket_type = input("\nTicket Type (e.g., technical issue, billing inquiry): ").strip()
        if ticket_type.lower() == 'quit':
            break
        
        subject = input("Subject (e.g., network problem, software bug): ").strip()
        if subject.lower() == 'quit':
            break
        
        description = input("Description: ").strip()
        if description.lower() == 'quit':
            break
        
        # Find similar tickets
        print("\n" + "-" * 70)
        print("SEARCHING FOR SIMILAR TICKETS...")
        print("-" * 70)
        
        similar_tickets = engine.find_similar_tickets(
            ticket_type=ticket_type,
            subject=subject,
            description=description,
            top_k=3
        )
        
        if similar_tickets:
            print(f"\n✓ Found {len(similar_tickets)} similar ticket(s)\n")
            print(engine.get_resolution_summary(similar_tickets))
        else:
            print("\n✗ No similar tickets found. This appears to be a new issue.")
            print("Recommendation: Escalate to support team for manual review.")
        
        # Ask to continue
        print("\n" + "-" * 70)
        continue_test = input("\nTest another ticket? (y/n): ").strip().lower()
        if continue_test != 'y':
            break
    
    print("\n" + "=" * 70)
    print("Thank you for using the NLP Engine!")
    print("=" * 70 + "\n")


def test_predefined():
    """
    Test with predefined test cases
    """
    print("\n" + "=" * 70)
    print(" " * 15 + "PREDEFINED TEST CASES")
    print("=" * 70)
    
    # Initialize engine
    engine = TicketNLPEngine()
    
    try:
        engine.load_data('processed_tickets.csv')
    except FileNotFoundError:
        print("\n✗ ERROR: processed_tickets.csv not found!")
        print("Please run: python preprocess_data.py first")
        return
    
    # Test cases
    test_cases = [
        {
            'name': 'Network Connectivity Issue',
            'ticket_type': 'technical issue',
            'subject': 'network problem',
            'description': 'cannot connect to wifi network having connectivity issues internet not working'
        },
        {
            'name': 'Application Crash',
            'ticket_type': 'technical issue',
            'subject': 'software bug',
            'description': 'application crashes when trying to save files getting unexpected errors'
        },
        {
            'name': 'Login Problem',
            'ticket_type': 'technical issue',
            'subject': 'account access',
            'description': 'unable to login to my account forgot password and reset option not working'
        },
        {
            'name': 'Product Setup',
            'ticket_type': 'technical issue',
            'subject': 'product setup',
            'description': 'need help setting up the product cannot find installation instructions'
        },
        {
            'name': 'Battery Issue',
            'ticket_type': 'technical issue',
            'subject': 'battery life',
            'description': 'battery draining very fast not lasting as long as before'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print("=" * 70)
        print(f"Type: {test_case['ticket_type']}")
        print(f"Subject: {test_case['subject']}")
        print(f"Description: {test_case['description']}")
        print("-" * 70)
        
        similar = engine.find_similar_tickets(
            ticket_type=test_case['ticket_type'],
            subject=test_case['subject'],
            description=test_case['description'],
            top_k=3
        )
        
        if similar:
            print(f"\n✓ Found {len(similar)} similar ticket(s)\n")
            for j, ticket in enumerate(similar, 1):
                print(f"Match {j} (Similarity: {ticket['similarity_score']:.1%})")
                print(f"  Subject: {ticket['subject']}")
                print(f"  Resolution: {ticket['resolution'][:100]}...")
                print()
        else:
            print("\n✗ No similar tickets found")
        
        input("\nPress Enter to continue to next test case...")
    
    print("\n" + "=" * 70)
    print("All test cases completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    import sys
    
    print("\nSelect test mode:")
    print("1. Interactive Testing (enter your own tickets)")
    print("2. Predefined Test Cases")
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == '1':
        test_interactive()
    elif choice == '2':
        test_predefined()
    elif choice == '3':
        test_predefined()
        test_interactive()
    else:
        print("Invalid choice. Running interactive mode...")
        test_interactive()
