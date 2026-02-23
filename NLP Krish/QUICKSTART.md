# Quick Start Guide

## 3-Step Setup (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Preprocess Data
```bash
python preprocess_data.py
```

Expected output:
```
============================================================
IT TICKET DATA PREPROCESSING
============================================================

[1/5] Reading data from: customer_support_tickets.csv
   ✓ Loaded 18763 rows, 17 columns

[2/5] Selecting required columns...
   ✓ Selected 5 columns

[3/5] Filtering data...
   Initial rows: 18763
   After removing null resolutions: 3245
   After removing empty resolutions: 3245
   After removing null descriptions: 3245

[4/5] Cleaning text data...
   ✓ Text cleaning completed
   ✓ Removed 0 duplicate entries

[5/5] Saving processed data to: processed_tickets.csv
   ✓ Saved 3245 processed tickets

============================================================
PREPROCESSING COMPLETE!
============================================================
```

### Step 3: Test the NLP Engine
```bash
python test_nlp.py
```

Choose option 1 for interactive testing or option 2 for predefined tests.

## Example Usage

### Interactive Test
```
Enter ticket details:

Ticket Type: technical issue
Subject: network problem  
Description: cannot connect to wifi internet not working

SEARCHING FOR SIMILAR TICKETS...
------------------------------------------------------------

✓ Found 3 similar ticket(s)

RECOMMENDED RESOLUTIONS (Based on Similar Tickets)
============================================================

Option 1 (Match: 78.5%, Priority: High)
Similar Issue: network problem
Resolution: check wifi settings restart router verify credentials
------------------------------------------------------------
```

### Python Code
```python
from nlp_engine import TicketNLPEngine

# Initialize
engine = TicketNLPEngine()
engine.load_data('processed_tickets.csv')

# Find similar tickets
results = engine.find_similar_tickets(
    ticket_type="technical issue",
    subject="software bug",
    description="application crashes when saving files",
    top_k=3
)

# Print results
for i, ticket in enumerate(results, 1):
    print(f"{i}. Similarity: {ticket['similarity_score']:.1%}")
    print(f"   Resolution: {ticket['resolution']}\n")
```

## Test Cases to Try

1. **Network Issue**
   - Type: `technical issue`
   - Subject: `network problem`
   - Description: `cannot connect to wifi`

2. **Software Bug**
   - Type: `technical issue`
   - Subject: `software bug`
   - Description: `application crashes when saving`

3. **Account Access**
   - Type: `technical issue`
   - Subject: `account access`
   - Description: `forgot password reset not working`

4. **Battery Problem**
   - Type: `technical issue`
   - Subject: `battery life`
   - Description: `battery draining very fast`

5. **Product Setup**
   - Type: `product inquiry`
   - Subject: `product setup`
   - Description: `need help installing product`

## What Gets Created

After running the scripts:
```
✓ processed_tickets.csv  - Cleaned dataset (3000+ tickets)
✓ nlp_model.pkl         - Trained model (optional, for faster loading)
```

## Common Issues

**No similar tickets found?**
- Try more descriptive descriptions
- Check if ticket type matches historical data
- Lower similarity threshold in nlp_engine.py

**Import errors?**
- Run: `pip install -r requirements.txt`
- Ensure Python 3.8+

**File not found?**
- Ensure `customer_support_tickets.csv` is in the same directory
- Run preprocessing first: `python preprocess_data.py`

## Next Steps

1. ✅ Test with your own ticket descriptions
2. ✅ Adjust similarity threshold if needed
3. ✅ Save model for faster loading: `engine.save_model()`
4. ✅ Integrate into your application

## Performance

- Preprocessing: ~5 seconds for 18K tickets
- Loading model: ~2 seconds
- Query time: < 0.1 seconds per ticket
- Memory: ~50MB

Enjoy using the NLP Engine! 🚀
