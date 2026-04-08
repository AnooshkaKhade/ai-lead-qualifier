# app.py

import streamlit as st
from utils.prompts import build_lead_prompt
from services.llm_service import get_llm_response
from utils.ui_helpers import copy_button

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Lead Qualifier",
    page_icon="🎯",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background-color: #0f1117;
        }

        /* Card style for result sections */
        .result-card {
            background-color: #1e2130;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 16px;
            border: 1px solid #2e3250;
        }

        /* Score badges */
        .badge-hot {
            background-color: #ff4b4b22;
            color: #ff4b4b;
            border: 1px solid #ff4b4b;
            padding: 6px 20px;
            border-radius: 20px;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
        }
        .badge-warm {
            background-color: #ffa50022;
            color: #ffa500;
            border: 1px solid #ffa500;
            padding: 6px 20px;
            border-radius: 20px;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
        }
        .badge-cold {
            background-color: #4b9fff22;
            color: #4b9fff;
            border: 1px solid #4b9fff;
            padding: 6px 20px;
            border-radius: 20px;
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        /* Section headers */
        .section-label {
            font-size: 13px;
            font-weight: 600;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }

        /* Divider */
        hr {
            border-color: #2e3250;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #161822;
            border-right: 1px solid #2e3250;
        }

        /* Input fields */
        .stTextInput input, .stTextArea textarea {
            background-color: #1e2130 !important;
            border: 1px solid #2e3250 !important;
            color: #fff !important;
            border-radius: 8px !important;
        }

        /* Button */
        .stFormSubmitButton button {
            background-color: #4b9fff !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            width: 100% !important;
        }
        .stFormSubmitButton button:hover {
            background-color: #2e7de0 !important;
        }
    </style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("Personalize the AI output for your use case.")
    st.divider()

    tone = st.selectbox(
        "🗣️ Response Tone",
        options=["Formal", "Friendly", "Direct"],
        help="Controls the tone of reply and follow-up messages"
    )

    industry = st.selectbox(
        "🏢 Industry",
        options=[
            "SaaS / Software",
            "Marketing & Advertising",
            "E-commerce",
            "Finance & Fintech",
            "Healthcare",
            "Real Estate",
            "Consulting & Professional Services",
            "Education & EdTech",
            "Manufacturing",
            "Other",
        ],
        help="Helps the AI personalize messages to industry context"
    )

    st.divider()
    st.markdown("#### 💡 Tips")
    st.caption("• Paste the lead's exact message for best results")
    st.caption("• Use **Direct** tone for cold outreach")
    st.caption("• Use **Formal** tone for enterprise leads")
    st.caption("• Use **Friendly** tone for SMB leads")

    st.divider()
    st.caption("Built with Streamlit + Groq LLaMA 3")


# ── Header ────────────────────────────────────────────────────
st.markdown("# 🎯 AI Lead Qualifier")
st.markdown("##### Classify leads instantly. Generate personalized outreach in seconds.")
st.divider()


# ── Main input form ───────────────────────────────────────────
with st.form("lead_form"):

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "👤 Contact Name",
            placeholder="e.g. Sarah Johnson"
        )

    with col2:
        company = st.text_input(
            "🏢 Company",
            placeholder="e.g. Acme Corp"
        )

    message = st.text_area(
        "💬 Lead Message / Inquiry",
        placeholder="Paste the lead's message or describe their inquiry here...",
        height=160
    )

    submitted = st.form_submit_button(
        "🔍 Analyze Lead",
        use_container_width=True
    )


# ── Processing ────────────────────────────────────────────────
if submitted:

    if not name.strip() or not company.strip() or not message.strip():
        st.warning("⚠️ Please fill in all fields before analyzing.")
        st.stop()

    with st.spinner("Analyzing lead..."):
        prompt = build_lead_prompt(name, company, message, tone, industry)
        raw    = get_llm_response(prompt)

    # ── Parse response ────────────────────────────────────────
    def extract(label: str, next_label: str | None, text: str) -> str:
        try:
            start = text.index(label) + len(label)
            end   = text.index(next_label) if next_label and next_label in text else len(text)
            return text[start:end].strip()
        except ValueError:
            return "Could not parse this section."

    lead_score   = extract("LEAD_SCORE:",        "REASONING:",          raw)
    reasoning    = extract("REASONING:",         "REPLY_MESSAGE:",      raw)
    reply_msg    = extract("REPLY_MESSAGE:",      "FOLLOW_UP_MESSAGE:",  raw)
    followup_msg = extract("FOLLOW_UP_MESSAGE:",  None,                  raw)

    score_clean  = lead_score.strip().upper()

    # ── Score badge ───────────────────────────────────────────
    badge_map = {
        "HOT":  ("badge-hot",  "🔴 HOT"),
        "WARM": ("badge-warm", "🟡 WARM"),
        "COLD": ("badge-cold", "🔵 COLD"),
    }
    badge_class, badge_label = badge_map.get(score_clean, ("badge-cold", "⚪ UNKNOWN"))

    # ── Results ───────────────────────────────────────────────
    st.divider()
    st.markdown("## 📊 Analysis Results")

    # Score + Reasoning card
    st.markdown(f"""
        <div class="result-card">
            <div class="section-label">Lead Score</div>
            <span class="{badge_class}">{badge_label}</span>
            <br><br>
            <div class="section-label">Reasoning</div>
            <p style="color:#ccc; margin:0">{reasoning}</p>
        </div>
    """, unsafe_allow_html=True)

    # Reply + Follow-up side by side
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
            <div class="section-label">💬 Suggested Reply</div>
        """, unsafe_allow_html=True)
        st.text_area("", value=reply_msg, height=200, key="reply_out")
        copy_button(reply_msg, "📋 Copy Reply")

    with col_b:
        st.markdown("""
            <div class="section-label">📅 Follow-up Message</div>
        """, unsafe_allow_html=True)
        st.text_area("", value=followup_msg, height=200, key="followup_out")
        copy_button(followup_msg, "📋 Copy Follow-up")

    # ── Footer ────────────────────────────────────────────────
    st.divider()
    st.caption("🎯 AI Lead Qualifier · Results are AI-generated · Always review before sending")
    