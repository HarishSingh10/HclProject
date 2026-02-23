"""
NLP Engine for IT Ticket Resolution Recommendation System
Uses TF-IDF vectorization and cosine similarity to find similar tickets
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class TicketNLPEngine:
    """
    NLP Engine for ticket similarity matching and resolution recommendation
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=2000,        # Vocabulary size
            stop_words='english',     # Remove common English words
            ngram_range=(1, 3),       # Use 1-word, 2-word, and 3-word phrases
            min_df=2,                 # Ignore terms that appear in less than 2 documents
            max_df=0.8,               # Ignore terms that appear in more than 80% of documents
            sublinear_tf=True         # Use logarithmic term frequency
        )
        self.ticket_vectors = None
        self.tickets_df = None
        
    def load_data(self, csv_file='processed_tickets.csv'):
        """
        Load preprocessed ticket data from CSV
        """
        import os
        
        if not os.path.exists(csv_file):
            print(f"\n✗ ERROR: {csv_file} not found!")
            print("\nYou need to run preprocessing first:")
            print("  python run_preprocessing.py")
            print("\nOr if you have the original CSV:")
            print("  python preprocess_data.py")
            raise FileNotFoundError(f"{csv_file} not found. Run preprocessing first.")
        
        print(f"\n[NLP Engine] Loading data from {csv_file}...")
        self.tickets_df = pd.read_csv(csv_file)
        print(f"[NLP Engine] Loaded {len(self.tickets_df)} tickets")
        
        # Create combined text with weighted features
        # Weight: Ticket Type (2x), Subject (3x), Description (1x)
        print("[NLP Engine] Creating weighted text features...")
        combined_texts = []
        
        for _, row in self.tickets_df.iterrows():
            ticket_type = str(row['Ticket Type']) if pd.notna(row['Ticket Type']) else ''
            subject = str(row['Ticket Subject']) if pd.notna(row['Ticket Subject']) else ''
            description = str(row['Ticket Description']) if pd.notna(row['Ticket Description']) else ''
            
            # Apply weights by repeating important fields
            combined = f"{ticket_type} {ticket_type} {subject} {subject} {subject} {description}"
            combined_texts.append(combined)
        
        # Vectorize the text data
        print("[NLP Engine] Vectorizing text using TF-IDF...")
        self.ticket_vectors = self.vectorizer.fit_transform(combined_texts)
        
        print(f"[NLP Engine] Vocabulary size: {len(self.vectorizer.vocabulary_)}")
        print(f"[NLP Engine] Vector shape: {self.ticket_vectors.shape}")
        print("[NLP Engine] ✓ Data loaded and vectorized successfully!\n")
        
    def find_similar_tickets(self, ticket_type, subject, description, top_k=3):
        """
        Find top K similar tickets based on cosine similarity
        
        Args:
            ticket_type: Type of the new ticket
            subject: Subject of the new ticket
            description: Description of the new ticket
            top_k: Number of similar tickets to return
            
        Returns:
            List of dictionaries containing similar tickets with similarity scores
        """
        if self.ticket_vectors is None or self.tickets_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Create combined text with same weights
        ticket_type = str(ticket_type) if ticket_type else ''
        subject = str(subject) if subject else ''
        description = str(description) if description else ''
        
        combined = f"{ticket_type} {ticket_type} {subject} {subject} {subject} {description}"
        
        # Vectorize the new ticket
        new_vector = self.vectorizer.transform([combined])
        
        # Calculate cosine similarity with all historical tickets
        similarities = cosine_similarity(new_vector, self.ticket_vectors)[0]
        
        # Get top K indices (sorted by similarity)
        top_indices = np.argsort(similarities)[::-1][:top_k * 2]  # Get extra candidates
        
        # Filter and prepare results
        results = []
        seen_resolutions = set()
        
        for idx in top_indices:
            if len(results) >= top_k:
                break
            
            similarity_score = similarities[idx]
            
            # Only include tickets with reasonable similarity
            if similarity_score > 0.05:
                ticket = self.tickets_df.iloc[idx]
                resolution = ticket['Resolution']
                
                # Avoid duplicate resolutions
                if resolution not in seen_resolutions:
                    results.append({
                        'ticket_type': ticket['Ticket Type'],
                        'subject': ticket['Ticket Subject'],
                        'description': ticket['Ticket Description'],
                        'resolution': resolution,
                        'priority': ticket['Ticket Priority'],
                        'similarity_score': float(similarity_score)
                    })
                    seen_resolutions.add(resolution)
        
        return results
    
    def get_resolution_summary(self, similar_tickets):
        """
        Create a comprehensive resolution summary from similar tickets
        
        Args:
            similar_tickets: List of similar ticket dictionaries
            
        Returns:
            Formatted resolution summary string
        """
        if not similar_tickets:
            return "No similar historical tickets found. Please contact support for assistance."
        
        summary = "RECOMMENDED RESOLUTIONS (Based on Similar Tickets)\n"
        summary += "=" * 60 + "\n\n"
        
        for i, ticket in enumerate(similar_tickets, 1):
            summary += f"Option {i} (Match: {ticket['similarity_score']:.1%}, Priority: {ticket['priority']})\n"
            summary += f"Similar Issue: {ticket['subject']}\n"
            summary += f"Resolution: {ticket['resolution']}\n"
            summary += "-" * 60 + "\n\n"
        
        summary += "Try these solutions in order. If issue persists, escalate to support team."
        
        return summary
    
    def save_model(self, filepath='nlp_model.pkl'):
        """Save the trained model to disk"""
        model_data = {
            'vectorizer': self.vectorizer,
            'ticket_vectors': self.ticket_vectors,
            'tickets_df': self.tickets_df
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"[NLP Engine] Model saved to {filepath}")
    
    def load_model(self, filepath='nlp_model.pkl'):
        """Load a trained model from disk"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.ticket_vectors = model_data['ticket_vectors']
        self.tickets_df = model_data['tickets_df']
        print(f"[NLP Engine] Model loaded from {filepath}")
    
    def get_statistics(self):
        """Get statistics about the loaded data"""
        if self.tickets_df is None:
            return "No data loaded"
        
        stats = {
            'total_tickets': len(self.tickets_df),
            'ticket_types': self.tickets_df['Ticket Type'].value_counts().to_dict(),
            'priorities': self.tickets_df['Ticket Priority'].value_counts().to_dict(),
            'vocabulary_size': len(self.vectorizer.vocabulary_) if self.vectorizer.vocabulary_ else 0
        }
        return stats


def demo():
    """
    Demo function to show how to use the NLP Engine
    """
    print("\n" + "=" * 60)
    print("NLP ENGINE DEMO")
    print("=" * 60)
    
    # Initialize engine
    engine = TicketNLPEngine()
    
    # Load data
    engine.load_data('processed_tickets.csv')
    
    # Display statistics
    stats = engine.get_statistics()
    print("\nEngine Statistics:")
    print(f"  Total Tickets: {stats['total_tickets']}")
    print(f"  Vocabulary Size: {stats['vocabulary_size']}")
    
    # Test with sample tickets
    print("\n" + "=" * 60)
    print("TEST CASE 1: Network Problem")
    print("=" * 60)
    
    similar = engine.find_similar_tickets(
        ticket_type="technical issue",
        subject="network problem",
        description="cannot connect to wifi network having connectivity issues",
        top_k=3
    )
    
    print(engine.get_resolution_summary(similar))
    
    print("\n" + "=" * 60)
    print("TEST CASE 2: Software Bug")
    print("=" * 60)
    
    similar = engine.find_similar_tickets(
        ticket_type="technical issue",
        subject="software bug",
        description="application crashes when trying to save files unexpected errors",
        top_k=3
    )
    
    print(engine.get_resolution_summary(similar))
    
    print("\n" + "=" * 60)
    print("TEST CASE 3: Account Access")
    print("=" * 60)
    
    similar = engine.find_similar_tickets(
        ticket_type="technical issue",
        subject="account access",
        description="unable to login forgot password reset not working",
        top_k=3
    )
    
    print(engine.get_resolution_summary(similar))
    
    # Save model
    print("\n" + "=" * 60)
    engine.save_model('nlp_model.pkl')
    print("=" * 60)


if __name__ == "__main__":
    demo()
