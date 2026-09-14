import streamlit as st
import pandas as pd
from groq import Groq
import plotly.express as px

st.set_page_config(page_title="PaytmZoop", page_icon="🅿️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600&display=swap');
:root { --navy: #002E6E; --cyan: #00BAF2; --bg: #F1F5F9; --border: #E2E8F0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1B1F3B; }
.stApp { background-color: var(--bg); }

.brand-text { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.6rem; color: var(--navy); }
.brand-text span { color: var(--cyan); }

.topbar { background: #FFFFFF; border-radius: 12px; padding: 14px 22px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; }

.card-white { background: #FFFFFF; border-radius: 16px; padding: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); height: 100%; }
.card-cyan { background: linear-gradient(135deg, #DFF6FF, #C9EDFB); border-radius: 16px; padding: 24px; height: 100%; }
.card-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 1.3rem; color: var(--navy); margin: 0 0 8px 0; }
.card-body { color: #475569; font-size: 0.95rem; line-height: 1.5; }
.hero-number { font-family: 'Poppins', sans-serif; font-size: 1.9rem; font-weight: 700; color: var(--navy); margin: 0; }

div[data-testid="stMetric"] { background-color: #FFFFFF; border: 1px solid var(--border); border-radius: 14px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
div[data-testid="stMetricValue"] { color: var(--navy); }

.stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid var(--border); }
.stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0; padding: 12px 22px; font-weight: 700; font-size: 1.1rem; color: #0F172A; }
.stTabs [aria-selected="true"] { color: #0F172A !important; border-bottom: 3px solid var(--cyan); }

div[data-testid="stChatInput"] {
    background: linear-gradient(135deg, #FFFFFF 0%, #EAF9FF 100%);
    border: 2px solid var(--cyan);
    border-radius: 999px;
    box-shadow: 0 6px 18px rgba(0,186,242,0.28);
    padding: 6px 10px;
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}
div[data-testid="stChatInput"]:focus-within {
    box-shadow: 0 8px 22px rgba(0,186,242,0.4);
    border-color: var(--navy);
}
div[data-testid="stChatInput"] textarea {
    font-size: 1.05rem !important;
    color: var(--navy) !important;
}
div[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--navy), var(--cyan)) !important;
    border-radius: 50% !important;
}
div[data-testid="stChatInput"] button svg { fill: #FFFFFF !important; }

button[kind="primary"] { background-color: var(--navy) !important; color: #fff !important; border-radius: 999px !important; border: none !important; font-weight: 600 !important; padding: 10px 28px !important; }
button[kind="primary"]:hover { background-color: #001F4D !important; }
button[kind="secondary"] { background-color: #fff !important; color: var(--navy) !important; border: 2px solid var(--navy) !important; border-radius: 999px !important; font-weight: 600 !important; padding: 8px 22px !important; }
button[kind="secondary"]:hover { background-color: #F0F4F8 !important; }
.stDownloadButton>button { background-color: var(--cyan) !important; color: #fff !important; border: none !important; border-radius: 999px !important; font-weight: 600 !important; padding: 8px 22px !important; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.write("")
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown('<div class="card-white">', unsafe_allow_html=True)
        st.markdown('<p class="brand-text">Paytm<span>Zoop</span></p>', unsafe_allow_html=True)
        st.caption("Log in to view your business dashboard")
        st.write("")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Log in", type="primary"):
            if username == "merchant" and password == "demo123":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Incorrect username or password.")
        st.caption("Demo login: merchant / demo123")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="card-cyan">
            <p class="card-title">Know your business at a glance</p>
            <p class="card-body">See what's driving your revenue, get plain-language advice grounded in your real sales data, and keep your GST records ready — all in one place.</p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

CATEGORY_COLORS = {"Grocery": "#00BAF2", "Electronics": "#002E6E", "Clothing": "#FF3278", "Stationery": "#9CA3AF"}

def format_inr(n):
    n = int(round(n)); s = str(n)
    if len(s) <= 3: return f"₹{s}"
    last3, rest = s[-3:], s[:-3]
    out = ""
    while len(rest) > 2:
        out = "," + rest[-2:] + out
        rest = rest[:-2]
    return f"₹{rest}{out},{last3}"

@st.cache_data
def load_data():
    df =pd.read_csv('Indian Retail Store.csv')
    df['visit_date'] = pd.to_datetime(df['visit_date'], format='%d-%m-%Y')
    return df

df = load_data()

def weekly_revenue_trend(df):
    return df.set_index('visit_date').resample('W')['total_amount'].sum()

def top_categories(df, n=5):
    return df.groupby('product_category')['total_amount'].sum().sort_values(ascending=False).head(n)

gst_rate_map = {'Grocery': 0.05, 'Electronics': 0.18, 'Clothing': 0.05, 'Stationery': 0.0}

def add_gst_columns(df, gst_rate_map):
    df['gst_rate'] = df['product_category'].map(gst_rate_map).fillna(0.18)
    df['taxable_value'] = df['total_amount'] / (1 + df['gst_rate'])
    df['tax_amount'] = df['total_amount'] - df['taxable_value']
    return df

df = add_gst_columns(df, gst_rate_map)
weekly = weekly_revenue_trend(df)
cats = top_categories(df)
top_pct = round(cats.iloc[0] / cats.sum() * 100, 1)

def build_prompt(question, weekly_data, top_cats, gst_summary):
    return f"""You are a business advisor for an Indian small merchant.
Use ONLY the data below. Keep it to 3-4 plain sentences, no headers or bullets.
Reference specific numbers, formatted with the ₹ symbol.

Weekly revenue: {weekly_data.to_dict()}
Top categories: {top_cats.to_dict()}
GST summary (sample): {gst_summary.to_dict()}

Merchant's question: {question}"""

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

top_left, top_right = st.columns([3, 1])
with top_left:
    st.markdown('<div class="topbar"><p class="brand-text" style="margin:0;">Paytm<span>Zoop</span></p></div>', unsafe_allow_html=True)
with top_right:
    st.write("")
    if st.button(f"Log out ({st.session_state.username})", type="secondary"):
        st.session_state.logged_in = False
        st.rerun()

left, right = st.columns([1.4, 1])
with left:
    st.markdown(f"""
    <div class="card-white">
        <p class="card-title">{cats.index[0]} drives {top_pct}% of your revenue</p>
        <p class="card-body">Out of {format_inr(df['total_amount'].sum())} total, tracked across {df['product_category'].nunique()} categories this month.</p>
    </div>
    """, unsafe_allow_html=True)
with right:
    st.markdown(f"""
    <div class="card-cyan">
        <p class="card-title">GST collected</p>
        <p class="hero-number">{format_inr(df['tax_amount'].sum())}</p>
        <p class="card-body">Ready to export anytime from the Tax & records tab.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
tab1, tab2, tab3 = st.tabs(["💬  Ask about your shop", "📈  How you're doing", "🧾  Tax & records"])

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    question = st.chat_input("Ask about your business...")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
        prompt = build_prompt(question, weekly, cats, df[['product_category','tax_amount']].head(5))
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_ai(prompt)
                st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

with tab2:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", format_inr(df['total_amount'].sum()))
    c2.metric("Top Category", cats.index[0], format_inr(cats.iloc[0]))
    c3.metric("This Week", format_inr(weekly.iloc[-1]))
    st.write("")
    fig1 = px.line(weekly, x=weekly.index, y=weekly.values, labels={'x':'Week','y':'Revenue (₹)'}, title="Weekly Revenue Trend", template="plotly_white")
    fig1.update_traces(line_color="#00BAF2", line_width=3)
    st.plotly_chart(fig1, use_container_width=True)
    fig2 = px.bar(cats, x=cats.index, y=cats.values, labels={'x':'Category','y':'Revenue (₹)'}, title="Top Categories", template="plotly_white")
    fig2.update_traces(marker_color=[CATEGORY_COLORS.get(c, "#9CA3AF") for c in cats.index])
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    c1.metric("Total Taxable Value", format_inr(df['taxable_value'].sum()))
    c2.metric("Total GST Collected", format_inr(df['tax_amount'].sum()))
    st.write("")
    st.dataframe(df[['product_category','total_amount','gst_rate','taxable_value','tax_amount']].head(20), use_container_width=True)
    st.download_button("⬇️ Download GST Data", df.to_csv(index=False), "gst_summary.csv")
