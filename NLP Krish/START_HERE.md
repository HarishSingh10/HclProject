# 🚀 START HERE - Quick Setup Guide

## Step 1: Install Dependencies (30 seconds)

```bash
pip install pandas numpy scikit-learn
```

OR

```bash
pip install -r requirements.txt
```

## Step 2: Run the System (One Command!)

```bash
python run.py
```

This will:
- ✓ Check if your CSV file exists
- ✓ Automatically preprocess the data
- ✓ Load the NLP engine
- ✓ Run a quick test
- ✓ Show you what to do next

## Alternative: Step-by-Step

If you prefer to run each step manually:

### Step 2a: Preprocess Data
```bash
python run_preprocessing.py
```

### Step 2b: Test the Engine
```bash
python test_nlp.py
```

## What You'll See

```
====================================================================
           IT TICKET NLP ENGINE - SETUP CHECK
====================================================================

[1/3] Checking for original dataset...
  ✓ customer_support_tickets.csv found

[2/3] Checking for preprocessed data...
  → Running preprocessing now...

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

[4/5] Cleaning text data...
   ✓ Text cleaning completed

[5/5] Saving processed data to: processed_tickets.csv
   ✓ Saved 3245 processed tickets

[3/3] Running NLP Engine Demo...
--------------------------------------------------------------------

[NLP Engine] Loading data from processed_tickets.csv...
[NLP Engine] Loaded 3245 tickets
[NLP Engine] Creating weighted text features...
[NLP Engine] Vectorizing text using TF-IDF...
[NLP Engine] Vocabulary size: 1847
[NLP Engine] Vector shape: (3245, 1847)
[NLP Engine] ✓ Data loaded and vectorized successfully!

✓ NLP Engine loaded successfully!
  Total tickets: 3245
  Vocabulary size: 1847

====================================================================
QUICK TEST: Network Problem
====================================================================

✓ Found 3 similar tickets!

Top recommendation:
  Similarity: 78.5%
  Resolution: check wifi settings restart router verify network credentials...

====================================================================
✓ ALL CHECKS PASSED!
====================================================================

You can now:
  1. Run interactive tests: python test_nlp.py
  2. Use the engine in your code (see README.md)
  3. Run full demo: python nlp_engine.py
```

## Troubleshooting

### Error: "customer_support_tickets.csv not found"
**Solution**: Make sure your CSV file is in the same directory as the Python scripts.

### Error: "ModuleNotFoundError: No module named 'pandas'"
**Solution**: Run `pip install pandas numpy scikit-learn`

### Error: "No similar tickets found"
**Solution**: This is normal if your test ticket is very different from historical data. Try different test cases.

## Next Steps

Once setup is complete:

1. **Interactive Testing**
   ```bash
   python test_nlp.py
   ```
   Enter your own ticket descriptions and see recommendations.

2. **Use in Your Code**
   ```python
   from nlp_engine import TicketNLPEngine
   
   engine = TicketNLPEngine()
   engine.load_data('processed_tickets.csv')
   
   results = engine.find_similar_tickets(
       ticket_type="technical issue",
       subject="software bug",
       description="app crashes when saving",
       top_k=3
   )
   
   for ticket in results:
       print(f"Resolution: {ticket['resolution']}")
       print(f"Similarity: {ticket['similarity_score']:.1%}\n")
   ```

3. **Read Documentation**
   - `README.md` - Complete technical docs
   - `QUICKSTART.md` - Quick reference
   - `PROJECT_SUMMARY.md` - Overview
   - `NLP_PIPELINE.md` - Architecture details

## Files Created

After running `python run.py`:
- ✓ `processed_tickets.csv` - Cleaned dataset (~3,000 tickets)
- ✓ NLP engine ready to use

## Support

If you encounter issues:
1. Check that `customer_support_tickets.csv` is in the current directory
2. Ensure Python 3.8+ is installed
3. Verify all dependencies are installed
4. Read the error message carefully - it usually tells you what's wrong

---

**Ready?** Just run: `python run.py`
