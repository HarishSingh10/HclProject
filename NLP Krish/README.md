# IT Ticket Resolution NLP Engine

NLP-powered ticket resolution recommendation system using TF-IDF vectorization and cosine similarity.

## Features

- **Text Preprocessing**: Advanced cleaning (removes emails, URLs, phone numbers, special characters)
- **TF-IDF Vectorization**: Converts text to numerical vectors with 1-3 word phrases
- **Cosine Similarity**: Finds most similar historical tickets
- **Weighted Matching**: Prioritizes ticket type and subject over description
- **Top-K Recommendations**: Returns top 3 similar tickets with resolutions
- **Resolution Summarization**: Combines multiple resolutions into actionable suggestions

## Dataset Columns

The system processes these 5 columns from your CSV:
- **Ticket Type**: Category of the issue (e.g., technical issue, billing inquiry)
- **Ticket Subject**: Brief summary of the problem
- **Ticket Description**: Detailed description of the issue
- **Resolution**: Solution that was applied
- **Ticket Priority**: Urgency level (Low, Medium, High, Critical)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Preprocess Data

```bash
python preprocess_data.py
```

This will:
- Read `customer_support_tickets.csv`
- Extract the 5 required columns
- Clean and preprocess text data
- Remove duplicates and invalid entries
- Save to `processed_tickets.csv`

### Step 2: Test the NLP Engine

**Option A: Interactive Testing**
```bash
python test_nlp.py
```
Choose option 1 to enter your own test tickets.

**Option B: Predefined Test Cases**
```bash
python test_nlp.py
```
Choose option 2 to run automated test cases.

### Step 3: Use in Your Code

```python
from nlp_engine import TicketNLPEngine

# Initialize engine
engine = TicketNLPEngine()

# Load preprocessed data
engine.load_data('processed_tickets.csv')

# Find similar tickets
similar = engine.find_similar_tickets(
    ticket_type="technical issue",
    subject="network problem",
    description="cannot connect to wifi",
    top_k=3
)

# Get resolution summary
summary = engine.get_resolution_summary(similar)
print(summary)

# Save trained model
engine.save_model('nlp_model.pkl')

# Load saved model later
engine.load_model('nlp_model.pkl')
```

## How It Works

### 1. Text Cleaning
```
Input: "I'm having an issue with the {product_purchased}. Email: user@example.com"
Output: "having issue product"
```

### 2. Feature Weighting
```
Combined Text = Type(2x) + Subject(3x) + Description(1x)
```
This ensures ticket type and subject have more influence on similarity matching.

### 3. TF-IDF Vectorization
- Converts text to numerical vectors
- Uses 1-3 word phrases (unigrams, bigrams, trigrams)
- Vocabulary size: 2000 features
- Removes common English stop words

### 4. Cosine Similarity
```
Similarity = cos(θ) = (A · B) / (||A|| × ||B||)
```
Ranges from 0 (completely different) to 1 (identical)

### 5. Ranking & Filtering
- Ranks all tickets by similarity score
- Filters out duplicates
- Returns top 3 unique resolutions
- Minimum threshold: 5% similarity

## Example Output

```
RECOMMENDED RESOLUTIONS (Based on Similar Tickets)
============================================================

Option 1 (Match: 78.5%, Priority: High)
Similar Issue: network problem
Resolution: check wifi settings restart router verify network credentials
------------------------------------------------------------

Option 2 (Match: 65.2%, Priority: Medium)
Similar Issue: connectivity issue
Resolution: reset network adapter update network drivers contact it support
------------------------------------------------------------

Option 3 (Match: 52.3%, Priority: Low)
Similar Issue: internet not working
Resolution: troubleshoot network connection check cable connections
------------------------------------------------------------

Try these solutions in order. If issue persists, escalate to support team.
```

## File Structure

```
.
├── customer_support_tickets.csv    # Original dataset
├── preprocess_data.py              # Data preprocessing script
├── processed_tickets.csv           # Cleaned dataset (generated)
├── nlp_engine.py                   # Core NLP engine
├── test_nlp.py                     # Testing interface
├── requirements.txt                # Python dependencies
├── nlp_model.pkl                   # Saved model (generated)
└── README.md                       # This file
```

## NLP Engine Parameters

```python
TfidfVectorizer(
    max_features=2000,      # Maximum vocabulary size
    stop_words='english',   # Remove common words
    ngram_range=(1, 3),     # Use 1-3 word phrases
    min_df=2,               # Ignore rare terms
    max_df=0.8,             # Ignore very common terms
    sublinear_tf=True       # Use log scaling
)
```

## Performance Metrics

- **Preprocessing**: ~18,000 tickets in < 5 seconds
- **Vectorization**: < 2 seconds
- **Query Time**: < 0.1 seconds per ticket
- **Memory Usage**: ~50MB for 18K tickets

## Customization

### Adjust Similarity Threshold
```python
# In nlp_engine.py, line ~120
if similarity_score > 0.05:  # Change this value (0.0 to 1.0)
```

### Change Number of Results
```python
similar = engine.find_similar_tickets(
    ticket_type="...",
    subject="...",
    description="...",
    top_k=5  # Change from 3 to any number
)
```

### Modify Feature Weights
```python
# In nlp_engine.py, line ~50
# Current: Type(2x) + Subject(3x) + Description(1x)
combined = f"{ticket_type} {ticket_type} {subject} {subject} {subject} {description}"

# Example: Equal weights
combined = f"{ticket_type} {subject} {description}"
```

## Troubleshooting

**Issue**: `FileNotFoundError: processed_tickets.csv`
**Solution**: Run `python preprocess_data.py` first

**Issue**: Low similarity scores
**Solution**: 
- Check if input text is properly cleaned
- Ensure historical data has similar ticket types
- Lower the similarity threshold

**Issue**: No results returned
**Solution**:
- Verify processed_tickets.csv has data
- Check if resolutions are not empty
- Try more descriptive ticket descriptions

## Next Steps

To integrate into a full application:
1. ✅ Data preprocessing complete
2. ✅ NLP engine ready
3. Add REST API (FastAPI/Flask)
4. Add database (SQLite/PostgreSQL)
5. Add web UI (Streamlit/React)
6. Add user authentication
7. Add admin dashboard

## License

MIT License - Feel free to use in your projects!
