import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def prepare_data(csv_path, output_csv):
    df = pd.read_csv(csv_path)
    cols = ['Ticket Type', 'Ticket Subject', 'Ticket Description', 'Resolution', 'Ticket Priority']
    df = df[cols]
    df = df.dropna(subset=['Resolution', 'Ticket Description'])
    
    df['combined_text'] = (
        df['Ticket Type'].fillna('') + " " +
        df['Ticket Subject'].fillna('') + " " +
        df['Ticket Description'].fillna('') + " " +
        df['Ticket Priority'].fillna('')
    )
    
    df['processed_text'] = df['combined_text'].apply(preprocess_text)
    df.to_csv(output_csv, index=False)
    return df

def build_nlp_engine(df, engine_path):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(df['processed_text'])
    
    with open(engine_path, 'wb') as f:
        pickle.dump({'vectorizer': vectorizer, 'tfidf_matrix': tfidf_matrix}, f)
    
    return vectorizer, tfidf_matrix

class RecommendationEngine:
    def __init__(self, data_path='processed_tickets.csv', engine_path='nlp_engine.pkl'):
        self.df = pd.read_csv(data_path)
        
        with open(engine_path, 'rb') as f:
            data = pickle.load(f)
            self.vectorizer = data['vectorizer']
            self.tfidf_matrix = data['tfidf_matrix']
            
        self.groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY")) if os.environ.get("GROQ_API_KEY") else None
            
    def get_recommendations(self, ticket_type, ticket_subject, ticket_description, ticket_priority, top_k=3):
        combined_input = f"{ticket_type} {ticket_subject} {ticket_description} {ticket_priority}"
        processed_input = preprocess_text(combined_input)
        input_vector = self.vectorizer.transform([processed_input])
        cosine_similarities = cosine_similarity(input_vector, self.tfidf_matrix).flatten()
        top_indices = cosine_similarities.argsort()[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            score = cosine_similarities[idx]
            match = self.df.iloc[idx]
            results.append({
                'similarity_score': round(score, 4),
                'suggested_resolution': match['Resolution'],
                'matched_ticket': {
                    'type': match['Ticket Type'],
                    'subject': match['Ticket Subject'],
                    'description': match['Ticket Description'],
                    'priority': match['Ticket Priority']
                }
            })
            
        return results

    def get_enhanced_recommendation(self, ticket_type, ticket_subject, ticket_description, ticket_priority, top_k=3):
        base_recs = self.get_recommendations(ticket_type, ticket_subject, ticket_description, ticket_priority, top_k)
        
        if not self.groq_client:
            return {
                "enhanced_resolution": "Groq API key not found. Please set GROQ_API_KEY environment variable.",
                "base_recommendations": base_recs
            }
            
        context_resolutions = "\n".join([
            f"- Suggestion {i+1} (Similarity Score: {rec['similarity_score']}): {rec['suggested_resolution']}"
            for i, rec in enumerate(base_recs)
        ])
        
        prompt = f"""
You are an expert customer support AI agent. A customer has submitted a new support ticket.
Below are {top_k} historical resolutions for similar tickets along with their similarity scores.

New Ticket Details:
- Type: {ticket_type}
- Subject: {ticket_subject}
- Priority: {ticket_priority}
- Description: {ticket_description}

Historical Resolutions:
{context_resolutions}

Your task is to review these historical resolutions, clean and synthesize them, and provide exactly 3 actionable suggestions for the user. 
Format your output strictly as a numbered list of 3 suggestions. For each suggestion, you MUST include the similarity score from the historical resolution it was derived from. Do not include any introductory or concluding conversational text, just the 3 suggestions.

Output Format Example:
1. [Suggestion Text] (Similarity Score: X.XXXX)
2. [Suggestion Text] (Similarity Score: X.XXXX)
3. [Suggestion Text] (Similarity Score: X.XXXX)
"""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful and professional customer support assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant",
                temperature=0.5,
                max_tokens=1024,
            )
            enhanced_resolution = chat_completion.choices[0].message.content
        except Exception as e:
            enhanced_resolution = f"Error generating enhanced resolution: {e}"
            
        return {
            "enhanced_resolution": enhanced_resolution,
            "base_recommendations": base_recs
        }

if __name__ == "__main__":
    input_csv = 'customer_support_tickets.csv'
    processed_csv = 'processed_tickets.csv'
    model_file = 'nlp_engine.pkl'
    
    if not os.path.exists(processed_csv) or not os.path.exists(model_file):
        df = prepare_data(input_csv, processed_csv)
        build_nlp_engine(df, model_file)
