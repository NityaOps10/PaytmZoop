
# PaytmZoop 🅿️

**An AI business partner for every Paytm merchant** — built for the Paytm "Build with AI. Solve for India." hackathon, Track 1: Merchant Growth AI.

## What it does

PaytmZoop turns a merchant's raw sales data into plain-language, actionable advice — not generic tips, but answers grounded in their actual numbers. It also auto-generates a simplified GST-ready bookkeeping summary from the same data, so merchants get both growth insights and tax-record help from one place.

## Key features

- **💬 Ask about your shop** — a chat interface where merchants ask business questions in plain language and get answers backed by their real sales figures (not generic ChatGPT-style advice)
- **📈 How you're doing** — a visual dashboard of weekly revenue trends and top-performing categories
- **🧾 Tax & records** — an auto-computed GST summary (taxable value, tax collected by category) with a one-click CSV export

## Why it's different from a generic AI chatbot

Every answer is generated from a prompt that injects the merchant's real computed numbers as context — the AI is instructed to reason only from that data, not general knowledge. This means answers cite specific figures (exact revenue, category %, tax amounts) instead of vague suggestions any business could receive.

## Tech stack

- **Frontend/backend:** Streamlit
- **AI:** Groq API (`openai/gpt-oss-20b`)
- **Data processing:** pandas
- **Charts:** Plotly

## Data note

This prototype uses a public, representative Indian retail sales dataset to demonstrate the reasoning engine. In production, this would connect directly to Paytm's existing merchant transaction data — no manual upload needed.

## Demo login

- Username: `merchant`
- Password: `demo123`

*(Demo-level authentication only — a production version would use proper secure login.)*

## Live demo

🔗 [Add your Streamlit Cloud link here once deployed]

## Disclaimer

GST calculations are simplified estimates for demonstration purposes, not compliance-certified filings.
