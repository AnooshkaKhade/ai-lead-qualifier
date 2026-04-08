import streamlit as st
import streamlit.components.v1 as components


def copy_button(text: str, button_label: str = "📋 Copy") -> None:
    """
    Renders a copy-to-clipboard button for the given text.
    Uses a small HTML/JS component — no extra libraries needed.

    Args:
        text:         The text to copy to clipboard
        button_label: Label shown on the button
    """

    # Escape backticks and backslashes so JS doesn't break
    safe_text = text.replace("\\", "\\\\").replace("`", "\\`")

    html_code = f"""
        <button
            onclick="navigator.clipboard.writeText(`{safe_text}`).then(() => {{
                this.innerText = '✅ Copied!';
                setTimeout(() => this.innerText = '{button_label}', 2000);
            }})"
            style="
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 6px 16px;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                margin-top: 4px;
            "
        >
            {button_label}
        </button>
    """

    components.html(html_code, height=45)
    