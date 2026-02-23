# NLP Engine Pipeline Architecture

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: Raw CSV Dataset                        │
│  (Ticket Type, Subject, Description, Resolution, Priority)       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 1: DATA PREPROCESSING                     │
├─────────────────────────────────────────────────────────────────┤
│  • Select 5 required columns                                     │
│  • Remove rows with missing resolutions                          │
│  • Text cleaning:                                                │
│    - Convert to lowercase                                        │
│    - Remove {product_purchased} placeholders                     │
│    - Remove emails, URLs, phone numbers                          │
│    - Remove special characters                                   │
│    - Remove standalone numbers                                   │
│    - Remove extra whitespace                                     │
│  • Remove duplicates                                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                OUTPUT: processed_tickets.csv                     │
│                    (~3,000 clean tickets)                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 2: FEATURE ENGINEERING                    │
├─────────────────────────────────────────────────────────────────┤
│  Weighted Text Combination:                                      │
│                                                                   │
│  Combined = Type(2x) + Subject(3x) + Description(1x)            │
│                                                                   │
│  Example:                                                         │
│  Type: "technical issue"                                         │
│  Subject: "network problem"                                      │
│  Description: "cannot connect wifi"                              │
│                                                                   │
│  Combined: "technical issue technical issue network problem      │
│             network problem network problem cannot connect wifi" │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 3: TF-IDF VECTORIZATION                   │
├─────────────────────────────────────────────────────────────────┤
│  Parameters:                                                      │
│  • max_features = 2000 (vocabulary size)                         │
│  • ngram_range = (1, 3) (1-3 word phrases)                       │
│  • stop_words = 'english' (remove common words)                  │
│  • min_df = 2 (ignore rare terms)                                │
│  • max_df = 0.8 (ignore very common terms)                       │
│  • sublinear_tf = True (log scaling)                             │
│                                                                   │
│  Output: Sparse Matrix [n_tickets × 2000]                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TRAINED NLP MODEL READY                       │
│              (Vectorizer + Historical Vectors)                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   NEW TICKET ARRIVES                             │
│  Type: "technical issue"                                         │
│  Subject: "software bug"                                         │
│  Description: "app crashes when saving"                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 4: QUERY PROCESSING                       │
├─────────────────────────────────────────────────────────────────┤
│  1. Apply same text cleaning                                     │
│  2. Apply same feature weighting                                 │
│  3. Transform using trained vectorizer                           │
│                                                                   │
│  New Vector: [1 × 2000]                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 5: SIMILARITY CALCULATION                 │
├─────────────────────────────────────────────────────────────────┤
│  Cosine Similarity:                                              │
│                                                                   │
│  similarity = (A · B) / (||A|| × ||B||)                          │
│                                                                   │
│  Calculate similarity between new ticket and ALL historical      │
│  tickets (vectorized operation - very fast!)                     │
│                                                                   │
│  Result: Array of similarity scores [0.0 to 1.0]                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 6: RANKING & FILTERING                    │
├─────────────────────────────────────────────────────────────────┤
│  1. Sort tickets by similarity (descending)                      │
│  2. Filter: similarity > 0.05 (5% threshold)                     │
│  3. Remove duplicate resolutions                                 │
│  4. Select top 3 unique results                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 7: RESOLUTION SUMMARY                     │
├─────────────────────────────────────────────────────────────────┤
│  Format results with:                                            │
│  • Similarity score (%)                                          │
│  • Priority level                                                │
│  • Similar ticket subject                                        │
│  • Resolution text                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   OUTPUT: TOP 3 RECOMMENDATIONS                  │
├─────────────────────────────────────────────────────────────────┤
│  Option 1 (Match: 78.5%, Priority: High)                        │
│  Similar Issue: software bug application crash                   │
│  Resolution: restart application clear cache update software     │
│  ─────────────────────────────────────────────────────────────  │
│  Option 2 (Match: 65.2%, Priority: Medium)                      │
│  Similar Issue: app not responding                               │
│  Resolution: check system requirements reinstall application     │
│  ─────────────────────────────────────────────────────────────  │
│  Option 3 (Match: 52.3%, Priority: Low)                         │
│  Similar Issue: software error                                   │
│  Resolution: contact support provide error logs                  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Text Preprocessing
```python
Input:  "I'm having an issue with the {product_purchased}. 
         Email: user@example.com. Call 123-456-7890"
         
Output: "having issue product"
```

### 2. Feature Weighting Strategy
```
Why weighted?
- Ticket Type: Broad category (important for filtering)
- Subject: Core issue summary (most important)
- Description: Detailed context (helpful but verbose)

Weight allocation: Type(2x) + Subject(3x) + Description(1x)
```

### 3. TF-IDF Vectorization
```
Term Frequency (TF): How often a word appears in a document
Inverse Document Frequency (IDF): How rare a word is across all documents

TF-IDF = TF × IDF

Example:
Word "network" in ticket about network issues:
- TF: High (appears multiple times)
- IDF: Medium (common in IT tickets)
- TF-IDF: Medium-High importance

Word "the" in any ticket:
- TF: High (appears often)
- IDF: Very Low (appears in almost all tickets)
- TF-IDF: Low importance (filtered out)
```

### 4. Cosine Similarity
```
Geometric interpretation:
- Treats documents as vectors in high-dimensional space
- Measures angle between vectors
- cos(0°) = 1.0 (identical)
- cos(90°) = 0.0 (completely different)

Example:
Ticket A: [0.5, 0.3, 0.8, 0.1, ...]
Ticket B: [0.4, 0.4, 0.7, 0.2, ...]
Similarity: 0.85 (85% match)
```

## Performance Characteristics

```
┌──────────────────────┬──────────────┬─────────────┐
│ Operation            │ Time         │ Complexity  │
├──────────────────────┼──────────────┼─────────────┤
│ Preprocessing        │ ~5 seconds   │ O(n)        │
│ Vectorization        │ ~2 seconds   │ O(n×m)      │
│ Single Query         │ <0.1 seconds │ O(n)        │
│ Batch Queries (100)  │ ~2 seconds   │ O(k×n)      │
└──────────────────────┴──────────────┴─────────────┘

n = number of tickets (~3000)
m = vocabulary size (2000)
k = number of queries
```

## Memory Usage

```
Component                Size
─────────────────────────────────────
Raw CSV                  ~5 MB
Processed CSV            ~1 MB
TF-IDF Vectors          ~25 MB (sparse)
Vocabulary              ~100 KB
Total Runtime           ~50 MB
```

## Accuracy Factors

```
High Similarity (>70%):
✓ Same ticket type
✓ Similar keywords in subject
✓ Common technical terms

Medium Similarity (40-70%):
~ Related issue category
~ Some keyword overlap
~ Different wording

Low Similarity (<40%):
✗ Different ticket types
✗ Unrelated issues
✗ No keyword overlap
```

## Optimization Techniques

1. **Sparse Matrix Storage**: Only store non-zero values
2. **Vectorized Operations**: NumPy/SciPy for speed
3. **Sublinear TF**: Log scaling prevents term frequency dominance
4. **Min/Max DF**: Filters noise and overly common terms
5. **N-grams**: Captures phrases like "network problem"

## Extension Points

```
Current: TF-IDF + Cosine Similarity
├─ Add: Word embeddings (Word2Vec, GloVe)
├─ Add: Transformer models (BERT, RoBERTa)
├─ Add: Category-specific models
├─ Add: User feedback loop
└─ Add: Active learning
```
