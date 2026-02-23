import json
import re
from groq import Groq
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

from dotenv import load_dotenv

load_dotenv()

# We initialize the Groq client
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

def preprocess_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def generate_ai_resolution(new_ticket_desc: str, historical_tickets: list):
    try:
        if not historical_tickets:
            historical_context = "No previous resolutions available."
        else:
            # 1. Prepare historical data in Pandas
            df = pd.DataFrame(historical_tickets)
            df['combined_text'] = df['description'].fillna('') + " " + df['resolution_text'].fillna('')
            df['processed_text'] = df['combined_text'].apply(preprocess_text)
            
            # 2. Add current unseen ticket
            new_processed = preprocess_text(new_ticket_desc)
            
            # 3. Vectorize and compute TF-IDF
            vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
            
            try:
                # Fit on history
                tfidf_matrix = vectorizer.fit_transform(df['processed_text'])
                new_vector = vectorizer.transform([new_processed])
                
                # similarities
                cosine_similarities = cosine_similarity(new_vector, tfidf_matrix).flatten()
                
                # Get top 5 matches
                top_k = 5
                top_indices = cosine_similarities.argsort()[-top_k:][::-1]
                
                context_parts = []
                for idx in top_indices:
                    score = cosine_similarities[idx]
                    match = df.iloc[idx]
                    context_parts.append(
                        f"- Suggestion (Similarity: {score:.4f}): {match['resolution_text']}"
                    )
                historical_context = "\n".join(context_parts)
            except Exception as e:
                # Fallback if TFIDF fails (e.g. empty vocab)
                historical_context = ""
                for t in historical_tickets[-5:]:
                    historical_context += f"- Fix: {t['resolution_text']}\n"
    
        # 4. Prompt for Groq
        prompt = f"""
You are an expert customer support AI agent. A user has submitted a new support issue.
Below are some top historical resolutions for similar issues retrieved from our database using TF-IDF similarity.

New User Issue: "{new_ticket_desc}"

Historical Resolutions:
{historical_context}

Your task is to review these historical resolutions, synthesize them, and provide EXACTLY 5 actionable suggestions for the user.
Return your output STRICTLY as a valid JSON array of 5 plain strings. Do NOT include markdown, metrics, or anything else outside the JSON block.

Example output:
[
  "Restart the router",
  "Check cable connections",
  "Clear browser cache",
  "Reset password",
  "Reinstall application"
]
"""
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024,
            stream=False,
            stop=None,
        )
        
        response_text = completion.choices[0].message.content.strip()
        response_text = re.sub(r"^```(?:json)?\n?", "", response_text)
        response_text = re.sub(r"\n?```$", "", response_text)
        response_text = response_text.strip()
        
        try:
            arr = json.loads(response_text)
            if isinstance(arr, list):
                return json.dumps(arr)
        except:
            pass
            
        return json.dumps([response_text])
            
    except Exception as e:
        print(f"Groq/NLP System Error: {e}")
        return json.dumps(["Our automated assistant is temporarily unavailable. A support rep will respond shortly."])

def get_similar_tickets(new_ticket_desc: str, historical_tickets: list, top_n: int = 3):
    return []
