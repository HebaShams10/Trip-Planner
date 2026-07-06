# 🌍 AI Trip Planner

An AI-powered travel planning assistant built with **Python**, **Streamlit**, **LangChain**, and **Groq LLM**. The application creates personalized travel itineraries after collecting the essential trip details from the user.

---

## ✨ Features

- 🤖 AI-powered travel assistant
- 🌍 Plans personalized trips
- 💰 Budget-aware recommendations
- 🏨 Hotel suggestions
- 🌦 Weather summary
- 📍 Attraction recommendations
- 🗓 Day-by-day itinerary generation
- 🚗 Transportation suggestions
- 💬 Conversational chat interface
- ⚡ Fast responses using Groq API

---

## 🧠 How It Works

The assistant follows a structured conversation flow.

Before generating any itinerary, it collects the following required information:

- Destination
- Number of travel days
- Budget
- Travel month
- Trip style
  - Relaxing
  - Adventure
  - Family
  - Luxury
  - Shopping
  - Food

If any required information is missing, the assistant asks only for the missing fields instead of generating incomplete plans.

Once all information is available, the assistant generates a complete travel itinerary.

---

## 📋 Generated Trip Includes

Each travel plan contains:

- Trip Overview
- Weather Summary
- Daily Schedule
- Hotel Recommendation
- Transportation Suggestions
- Estimated Daily Cost
- Estimated Total Budget
- Extra Travel Tips

---

## 🛠 Technologies Used

- Python
- Streamlit
- LangChain
- LangChain Core
- LangChain Community
- LangChain Groq
- Groq API
- Python Dotenv

---

## 📂 Project Structure

```
Trip-Planner/
│
├── app.py
├── requirements.txt
│
└── ChatBot/
    ├── chain.py
    ├── config.py
    ├── llm.py
    ├── memory.py
    ├── prompt.py
    ├── rate_limit.py
    ├── resolve.py
    ├── retry.py
    ├── shortcuts.py
    └── tracing.py
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/HebaShams10/Trip-Planner.git
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

## 📸 Screenshots

Screenshots will be added soon.

---

## 📌 Future Improvements

- Flight recommendations
- Restaurant recommendations
- Interactive maps
- Multi-language support
- Travel expense breakdown
- PDF itinerary export

---

## 👩‍💻 Author

**Heba Shams**

GitHub: https://github.com/HebaShams10
