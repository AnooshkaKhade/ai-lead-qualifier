# 🎯 AI Lead Qualifier

An AI-powered Streamlit app that classifies sales leads and generates 
personalized outreach messages instantly.

## Features

- ✅ Classifies leads as Hot / Warm / Cold with reasoning
- ✅ Generates personalized reply messages
- ✅ Generates follow-up messages
- ✅ Tone selector — Formal / Friendly / Direct
- ✅ Industry context for sharper personalization
- ✅ Copy-to-clipboard for all outputs

## Tech Stack

- Python 3.11+
- Streamlit
- Groq API (LLaMA 3.3 70B)
- python-dotenv

## Local Setup

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-lead-qualifier.git
cd ai-lead-qualifier

### 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Set up your API key

Get a free Groq API key at: https://console.groq.com

Create a .env file in the project root:
GROQ_API_KEY=your_groq_api_key_here

Note: Never commit your .env file. It is already in .gitignore.

### 5. Run the app
streamlit run app.py

## Project Structure

ai-lead-qualifier/
│
├── app.py                  ← Streamlit UI
├── requirements.txt        ← Dependencies
├── .env                    ← Your API key (not committed)
├── .gitignore
├── README.md
│
├── services/
│   └── llm_service.py      ← Groq API calls
│
└── utils/
    ├── prompts.py          ← Prompt templates
    └── ui_helpers.py       ← Copy button helper

## Deployment

This app is deployed on Streamlit Cloud.
Live demo: [ADD YOUR LINK AFTER DEPLOYMENT]

## Important Notes

- API keys are managed via environment variables
- Never commit your .env file
- For deployment, add GROQ_API_KEY in Streamlit Cloud secrets