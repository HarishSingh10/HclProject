"""
NLP Recommendation Engine
Uses TF-IDF and Cosine Similarity for ticket resolution matching
"""
import json
import re
from typing import List, Dict, Tuple
from collections import Counter
import math

class NLPRecommendationEngine:
    def __init__(self, resolutions_file: str):
        self.resolutions_file = resolutions_file
        self.resolutions = self.load_resolutions()
        self.vocabulary = self.build_vocabulary()
        self.tfidf_matrix = self.compute_tfidf_matrix()
    
    def load_resolutions(self) -> List[Dict]:
        """Load resolutions from JSON file"""
        try:
            with open(self.resolutions_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Text preprocessing: lowercase, remove special chars, tokenize
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Tokenize
        tokens = text.split()
        
        # Remove stop words (simple list)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                     'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her'}
        
        tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
        
        return tokens
    
    def build_vocabulary(self) -> set:
        """Build vocabulary from all resolutions"""
        vocab = set()
        for res in self.resolutions:
            tokens = self.preprocess_text(res['issue'] + ' ' + res['resolution'])
            vocab.update(tokens)
        return vocab
    
    def compute_tf(self, tokens: List[str]) -> Dict[str, float]:
        """Compute Term Frequency"""
        tf = Counter(tokens)
        total = len(tokens)
        return {word: count / total for word, count in tf.items()}
    
    def compute_idf(self) -> Dict[str, float]:
        """Compute Inverse Document Frequency"""
        doc_count = len(self.resolutions)
        word_doc_count = Counter()
        
        for res in self.resolutions:
            tokens = set(self.preprocess_text(res['issue'] + ' ' + res['resolution']))
            word_doc_count.update(tokens)
        
        idf = {}
        for word in self.vocabulary:
            idf[word] = math.log(doc_count / (1 + word_doc_count.get(word, 0)))
        
        return idf
    
    def compute_tfidf_matrix(self) -> List[Dict[str, float]]:
        """Compute TF-IDF matrix for all resolutions"""
        idf = self.compute_idf()
        tfidf_matrix = []
        
        for res in self.resolutions:
            tokens = self.preprocess_text(res['issue'] + ' ' + res['resolution'])
            tf = self.compute_tf(tokens)
            
            tfidf = {}
            for word in self.vocabulary:
                tfidf[word] = tf.get(word, 0) * idf.get(word, 0)
            
            tfidf_matrix.append(tfidf)
        
        return tfidf_matrix
    
    def compute_query_tfidf(self, query: str) -> Dict[str, float]:
        """Compute TF-IDF for query"""
        tokens = self.preprocess_text(query)
        tf = self.compute_tf(tokens)
        idf = self.compute_idf()
        
        tfidf = {}
        for word in self.vocabulary:
            tfidf[word] = tf.get(word, 0) * idf.get(word, 0)
        
        return tfidf
    
    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Compute cosine similarity between two vectors"""
        # Dot product
        dot_product = sum(vec1.get(word, 0) * vec2.get(word, 0) for word in self.vocabulary)
        
        # Magnitudes
        mag1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        mag2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        return dot_product / (mag1 * mag2)
    
    def get_recommendations(self, description: str, category: str, top_k: int = 3) -> List[Dict]:
        """
        Get top-k recommendations based on description and category
        """
        if not self.resolutions:
            return []
        
        # Compute query TF-IDF
        query_tfidf = self.compute_query_tfidf(description)
        
        # Compute similarities
        similarities = []
        for i, res in enumerate(self.resolutions):
            # Base similarity from TF-IDF
            similarity = self.cosine_similarity(query_tfidf, self.tfidf_matrix[i])
            
            # Boost score if category matches
            if res['category'].lower() == category.lower():
                similarity *= 1.5
            
            # Boost score for exact keyword matches
            desc_lower = description.lower()
            issue_lower = res['issue'].lower()
            
            if issue_lower in desc_lower or desc_lower in issue_lower:
                similarity *= 1.3
            
            similarities.append((similarity, res))
        
        # Sort by similarity and return top-k
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        return [
            {
                **res,
                'similarity_score': round(score * 100, 2)
            }
            for score, res in similarities[:top_k] if score > 0
        ]

# API endpoint for recommendations
def get_nlp_recommendations(description: str, category: str, resolutions_file: str) -> List[Dict]:
    """Get NLP-based recommendations"""
    engine = NLPRecommendationEngine(resolutions_file)
    return engine.get_recommendations(description, category)
