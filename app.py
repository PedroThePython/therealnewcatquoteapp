import random
import requests
import streamlit as st

CATFACT_API = "https://catfact.ninja/fact"

FALLBACK_QUOTES = [
    "Cats sleep 12–16 hours a day. Honestly, goals.",
    "A group of cats is called a clowder.",
    "Cats have whiskers on the back of their front legs, too.",
    "A cat’s purr can vibrate at a frequency linked to healing.",
    "Most cats don’t taste sweetness.",
]

@st.cache_data(ttl=60)  # cache for 60s to avoid hammering the API
def fetch_cat_quote() -> str:
    """Fetch a random cat fact (used here as a cat 'quote')."""
    try:
        r = requests.get(CATFACT_API, timeout=5)
        r.raise_for_status()
        data = r.json()
        fact = data.get("fact")
        if not fact or not isinstance(fact, str):
            raise ValueError("Unexpected API response shape")
        return fact.strip()
    except Exception:
        return random.choice(FALLBACK_QUOTES)

st.set_page_config(page_title="Random Cat Quote", page_icon="🐾")

st.title("🐾 Random Cat Quote")

if "quote" not in st.session_state:
    st.session_state.quote = fetch_cat_quote()

st.write(f"**“{st.session_state.quote}”**")

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("New quote"):
        # clear cache to force a fresh request immediately
        fetch_cat_quote.clear()
        st.session_state.quote = fetch_cat_quote()

with col2:
    st.caption("Source: catfact.ninja (with local fallback if the API is unavailable).")
