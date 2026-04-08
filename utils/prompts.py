# utils/prompts.py

def build_lead_prompt(name: str, company: str, message: str, tone: str, industry: str) -> str:
    """
    Builds a structured prompt for lead qualification and message generation.
    
    Args:
        name:     Lead's name
        company:  Lead's company
        message:  Lead's inquiry or message
        tone:     Communication tone (Formal / Friendly / Direct)
        industry: Industry context for personalization
    
    Returns:
        A complete prompt string ready to send to the LLM
    """

    tone_instructions = {
        "Formal": (
            "Use professional, corporate language. "
            "Avoid contractions. Be respectful and structured."
        ),
        "Friendly": (
            "Use warm, conversational language. "
            "Be approachable and personable. Use natural phrasing."
        ),
        "Direct": (
            "Be concise and to the point. "
            "Skip pleasantries. Focus on value and next steps."
        ),
    }

    tone_guide = tone_instructions.get(tone, tone_instructions["Formal"])

    prompt = f"""
You are an expert B2B sales assistant specializing in {industry}.

Your job is to analyze an incoming sales lead and produce three things:
1. A lead classification with reasoning
2. A personalized reply to the lead
3. A follow-up message to send later

---

LEAD DETAILS:
- Name: {name}
- Company: {company}
- Message: {message}
- Industry: {industry}

---

TONE INSTRUCTIONS:
{tone_guide}

---

CLASSIFICATION RULES:
- HOT: Lead shows clear buying intent, urgency, or specific ask. Needs immediate action.
- WARM: Lead is interested but vague, exploring, or not yet ready to commit.
- COLD: Lead is early-stage, low intent, generic inquiry, or unlikely to convert soon.

---

OUTPUT FORMAT (follow this exactly, no deviations):

LEAD_SCORE: [HOT or WARM or COLD]

REASONING: [2-3 sentences explaining why this score was given based on the message]

REPLY_MESSAGE:
[A personalized reply to send to this lead right now. Match the tone instructions above.]

FOLLOW_UP_MESSAGE:
[A follow-up message to send 3-5 days later if they don't respond. Match the tone.]

---

Important:
- Do NOT add any text before LEAD_SCORE
- Do NOT add explanations outside the format
- Keep REPLY and FOLLOW_UP under 150 words each
- Be specific to the lead's message, not generic
"""

    return prompt.strip()
