# 🎫 IT Ticket Resolution System

A modern, AI-powered IT ticket management system with NLP-based recommendations, FastAPI backend, and beautiful Streamlit UI.

## 🏗️ System Architecture

```
┌──────────────────────────────┐
│        STREAMLIT UI          │
│------------------------------│
│ 🔐 User Portal               │
│ 👨‍💼 Admin Portal              │
│ 📝 Ticket Submission          │
│ 💡 Suggestions Display        │
│ 📊 Analytics Dashboard        │
└──────────────┬───────────────┘
               │ REST API Calls
               ▼
┌──────────────────────────────┐
│      FASTAPI BACKEND         │
│------------------------------│
│ 🔑 Authentication Module     │
│ 🎫 Ticket Management Service │
│ 🤖 Recommendation Controller │
│ 👨‍💼 Admin Management Module   │
│ 📈 Analytics Service          │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│   NLP RECOMMENDATION ENGINE  │
│------------------------------│
│ 📝 Text Preprocessing        │
│ 🔢 TF-IDF Generator          │
│ 📐 Cosine Similarity Engine  │
│ 🎯 Ranking & Selection       │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│         DATABASE             │
│------------------------------│
│ 👥 Users                     │
│ 🎫 Tickets                   │
│ 💡 Resolutions               │
│ 📊 Status History            │
└──────────────────────────────┘
```

## ✨ Features

### 🎨 Modern UI/UX
- Dynamic Animated Backgrounds with gradient shifts
- Glass Morphism Design with blur effects
- Smooth Animations and transitions
- Icon-Rich Interface

### 🤖 AI-Powered Recommendations
- NLP Engine with TF-IDF
- Cosine Similarity matching
- Smart Ranking algorithm
- Top-3 Suggestions

## 🚀 Running the Application

```bash
python -m streamlit run app.py
```

## 🔑 Default Credentials

**Admin:** admin / admin123
**User:** user / user123

---

**Built with ❤️ using Streamlit, FastAPI, and NLP**
