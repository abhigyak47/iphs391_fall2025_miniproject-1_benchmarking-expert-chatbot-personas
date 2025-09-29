#!/usr/bin/env python3
"""
run_chatbot_fixed.py

Fix: Use Gradio Chatbot with type="messages" consistently.
- UI state is a list of {"role": "...", "content": "..."} dicts.
- Converts persisted conversation to messages format (filters out "system" for UI).

Setup:
  pip install openai gradio python-dotenv
  export OPENAI_API_KEY="sk-..."
"""

from pathlib import Path
import json
import os
import sys
from typing import List, Dict

# Optional .env support if installed
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

import gradio as gr
from openai import OpenAI

SCRIPT_DIR = Path(__file__).resolve().parent
PROMPT_PATH = SCRIPT_DIR / "prompt_persona.txt"
HISTORY_PATH = SCRIPT_DIR / "chat_history.json"

# ----- Config -----
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_TOKEN")

if not OPENAI_API_KEY:
    sys.stderr.write(
        "\nERROR: Missing OpenAI API key.\n"
        "Set an environment variable OPENAI_API_KEY (or OPENAI_TOKEN), e.g.:\n"
        "  export OPENAI_API_KEY='sk-...'\n\n"
    )
    sys.exit(1)

# Read the persona/system prompt
try:
    prompt_text = PROMPT_PATH.read_text(encoding="utf-8")
except FileNotFoundError:
    sys.stderr.write(
        f"\nERROR: '{PROMPT_PATH.name}' not found next to this script.\n"
        "Please create it and put your master prompt inside.\n"
    )
    sys.exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)

def load_history() -> List[Dict[str, str]]:
    """Load saved conversation history if it exists; else start with system message."""
    if HISTORY_PATH.exists():
        try:
            data = json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except Exception:
            pass
    # Seed with system persona
    return [{"role": "system", "content": prompt_text}]

def save_history(conv: List[Dict[str, str]]) -> None:
    try:
        HISTORY_PATH.write_text(json.dumps(conv, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"Warning: couldn't save history: {e}", file=sys.stderr)

# Shared conversation state (persists to disk on each message)
conversation: List[Dict[str, str]] = load_history()

def ui_messages_from_conversation(conv: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter to only user/assistant for the UI Chatbot (type='messages')."""
    return [m for m in conv if m.get("role") in ("user", "assistant")]

def llm_reply(user_message: str) -> str:
    """Send the full conversation (plus the new user message) to the API and return the assistant reply."""
    conversation.append({"role": "user", "content": user_message})
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=conversation,
            temperature=1.1,
            top_p=0.95,
            presence_penalty=0.4,
            frequency_penalty=0.2,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"(Error from model: {e})"
    conversation.append({"role": "assistant", "content": reply})
    save_history(conversation)
    return reply

def on_send(message: str, messages: List[Dict[str, str]]):
    """Gradio handler: takes the latest user message and the UI messages list (role/content dicts)."""
    if not message:
        return messages, gr.update(value="")
    reply = llm_reply(message)
    messages = messages + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return messages, gr.update(value="")

def on_clear():
    """Clear both UI and persisted history (keep system prompt in persisted conversation)."""
    global conversation
    conversation = [{"role": "system", "content": prompt_text}]
    save_history(conversation)
    try:
        if HISTORY_PATH.exists():
            HISTORY_PATH.unlink()
    except Exception:
        pass
    # Return empty UI messages list
    return []

with gr.Blocks(title="Guru - Travel Guide", fill_height=True, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Guru - Travel Guide")
    gr.Markdown(
        "Loads persona from **prompt_persona.txt**. "
        "History persists to **chat_history.json** in this folder."
    )
    chatbot = gr.Chatbot(
        value=ui_messages_from_conversation(conversation),
        type="messages",      # IMPORTANT: Messages format
        height=500,
        show_copy_button=True,
    )
    with gr.Row():
        msg = gr.Textbox(placeholder="Type your message...", scale=8)
        send_btn = gr.Button("Send", variant="primary", scale=1)
    with gr.Row():
        clear_btn = gr.Button("Clear chat (also clears saved history)", variant="secondary")
    with gr.Accordion("Settings", open=False):
        gr.Markdown(
            f"**Model:** {MODEL_NAME}  \n"
            "To change, set the `OPENAI_MODEL` environment variable."
        )

    # Wire events
    msg.submit(on_send, [msg, chatbot], [chatbot, msg])
    send_btn.click(on_send, [msg, chatbot], [chatbot, msg])
    clear_btn.click(on_clear, outputs=[chatbot])

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
