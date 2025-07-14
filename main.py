from __future__ import annotations

import json
import random
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import streamlit as st

from prompts import *

_SESSION_KEYS = {
    "chat_history": list[dict[str, str]],
    "new_user_input": str,
    "new_assistant_output": str,
}

DATA_DIR = Path()


def init_state() -> None:
    """Initialise ``st.session_state`` with safe defaults once per session."""
    for key, default in _SESSION_KEYS.items():
        st.session_state.setdefault(key, default())


def add_turn() -> None:
    """Append the user/assistant turn if both textareas are non‑empty."""
    user, assistant = (
        st.session_state.new_user_input.strip(),
        st.session_state.new_assistant_output.strip(),
    )

    if not (user and assistant):
        st.warning("Both the User Prompt and Assistant Response are required", icon="⚠️")
        return

    st.session_state.chat_history.append({"user_input": user, "assistant_output": assistant})
    st.session_state.new_user_input = ""
    st.session_state.new_assistant_output = ""


def remove_turn(idx: int) -> None:
    """Delete the *idx*‑th turn from the history."""
    try:
        st.session_state.chat_history.pop(idx)
    except IndexError:
        st.error("Invalid turn index", icon="❌")


@lru_cache(maxsize=None)
def load_jsonl(file_name: str, key: str) -> list[str]:
    """Read a ``.jsonl`` file once and cache the requested *key* field."""
    path = file_name
    if not path.exists():
        st.error(f"File not found: {path}")
        return []

    with path.open("r", encoding="utf‑8") as fp:
        return [json.loads(line).get(key, "") for line in fp if key in line]


def chat_history_fragment(*, max_turns: int = 20) -> None:
    """Display a collapsible summary of recent chat turns."""
    for idx, turn in enumerate(st.session_state.chat_history[-max_turns:]):
        with st.expander(f"Turn {idx + 1}"):
            st.markdown(f"**User:** {turn['user_input']}")
            st.markdown(f"**Assistant:** {turn['assistant_output']}")
            st.button(
                "🗑️ Remove",
                key=f"rm_{idx}",
                help="Delete this turn",
                on_click=remove_turn,
                args=(idx,),
                use_container_width=True
            )


def add_manual_turn_fragment() -> None:
    """Render controls for *manual* turn entry."""
    with st.expander("Add Turns Manually"):
        chat_history_fragment()
        with st.form("add_turn_form", clear_on_submit=False):
            st.text_area("User Input", key="new_user_input", height=80, placeholder="Type the customer's message…")
            st.text_area("Assistant Output", key="new_assistant_output", height=160,
                         placeholder="Type your assistant’s reply…")
            st.form_submit_button("Add Turn", on_click=add_turn)


def add_auto_turn_fragment(title: str, assistant_name: str, examples: str, turns_to_generate: int) -> None:
    """Show the LLM prompt for *automatic* turn generation."""
    prompt = SYNTHETIC_DATA_PROMPT.format(
        n=turns_to_generate,
        assistant_name=assistant_name,
        title=title,
        examples=examples,
    ).strip()
    st.code(prompt, wrap_lines=True, height=200)
    st.text_area(
        "Reviewed Synthetic Conversation",
        key=f"{assistant_name.lower()}_synthetic_conversation",
        height=200,
        placeholder="Paste the generated conversation from LLM…",
    )


def render_ten_classification_page() -> None:
    st.subheader("Fixed Instructions")
    with st.expander("General Instructions"):
        st.markdown(TEN_GENERAL_INSTRUCTIONS)
    with st.expander("Detailed Instructions"):
        st.markdown(TEN_DETAILED_INSTRUCTIONS)

    st.subheader("Per-Sample Section")
    render_ten_classification_form()


@dataclass
class ProductDetailInput:
    """Container for product detail fields."""

    keywords: str = ""
    title: list[str] = None
    bullet_points: list[str] = None
    product_type: list[str] = None
    gl_product_type: list[str] = None
    brand: list[str] = None
    color: list[str] = None
    size: list[str] = None
    ground_truth: str = ""

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=2, ensure_ascii=False)


def render_ten_classification_form() -> None:
    with st.form("ten_form"):
        data = ProductDetailInput(
            keywords=st.text_input("Search Query"),
            title=st.text_area("Product Title").strip().splitlines(),
            brand=st.text_area("Product Brand").strip().splitlines(),
            bullet_points=st.text_area("Product Bullet Points").strip().splitlines(),
            product_type=st.text_area("Product Type").strip().splitlines(),
            gl_product_type=st.text_area("General Ledger Category").strip().splitlines(),
            color=st.text_area("Product Color").strip().splitlines(),
            size=st.text_area("Product Size").strip().splitlines(),
            ground_truth=st.selectbox("ESCI Categories", TEN_ESCI_CATEGORIES),
        )

        if st.form_submit_button("Generate Product JSON", use_container_width=True):
            with st.expander("JSON Output"):
                st.code(data.to_json(), language="json", wrap_lines=True)
    st.download_button(
        "📥 Download JSON",
        data=data.to_json(),
        file_name="product_details.json",
        mime="application/json",
        use_container_width=True
    )


def render_intent_classification_page() -> None:
    st.subheader("Fixed Instructions")
    with st.expander("General Instructions"):
        st.markdown(INTENT_GENERAL_INSTRUCTIONS)
    with st.expander("Intent Definitions"):
        st.code(INTENT_DEFINITION, language="xml")
    with st.expander("Ambiguity Level Definitions"):
        st.code(INTENT_AMBIGUITY_LEVEL_DEFINITION, language="xml")
    with st.expander("K-Shot Examples"):
        st.code(INTENT_K_SHOT_EXAMPLES, language="xml")
    with st.expander("Instruction Reminder"):
        st.markdown(INTENT_INSTRUCTIONS_REMINDER)

    st.subheader("Per-Sample Section")
    render_intent_classification_form()


def _auto_examples(file_name: str, history_key: str, k: int, title_key: str, divider: str = "\n---\n\n", ) -> str:
    # path = DATA_DIR / file_name
    # if not path.exists():
    #     st.error(f"File not found: {path}")
    #     # return ""

    examples: list[str] = []
    with open(file_name, "r", encoding="utf-8") as fp:
        for raw in fp:
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError:
                continue

            history = obj.get(history_key)
            if not history:
                continue

            title = obj.get(title_key, "").strip()
            if title and history:
                chat_turn = f"Product: {title}\n\nConversation:\n {history}"

            examples.append(chat_turn)

    if not examples:
        return ""

    chosen = random.sample(examples, k) if len(examples) >= k else examples
    return divider.join(chosen)


def render_intent_classification_form() -> None:
    st.text_input("Product Attributes", key="intent_product_attributes")

    generation_mode = st.radio(
        "Conversation history generation approach",
        ("Automatic", "Manual"),
        horizontal=True,
    )

    if generation_mode == "Automatic":
        with st.expander("Generate Prompt"):
            with st.expander("Advanced"):
                examples_to_retrieve = st.number_input("Examples to retrieve", value=5)
                turns_to_generate = st.number_input("Turns to generate", value=3)

            examples = _auto_examples("intentData_100.jsonl", "ChatHistory", int(examples_to_retrieve),
                                      "ProductAttributes")
            add_auto_turn_fragment(
                st.session_state.intent_product_attributes,
                "Assistant",
                examples,
                int(turns_to_generate),
            )
    else:
        init_state()
        add_manual_turn_fragment()

    st.text_input("Customer Utterance", key="intent_customer_utterance")
    st.selectbox("Intent Option", INTENT_OPTIONS, key="intent_options")
    st.selectbox("Ambiguity Level", INTENT_AMBIGUITY_LEVELS, key="intent_ambiguity_level")

    if st.button("Generate Intent Classification JSON", use_container_width=True):
        synthetic_conv_key = "assistant_synthetic_conversation"
        conversation_history = (
                st.session_state.get(synthetic_conv_key)
                or "\n".join(
            f"Customer: {c['user_input']}\nAssistant: {c['assistant_output']}" for c in
            st.session_state.get('chat_history', [])
        )
        )
        benchmark = {
            "ProductAttributes": f"<product_details>{st.session_state.intent_product_attributes}</product_details>",
            "ChatHistory": f"<conversation_history>{conversation_history}</conversation_history>",
            "CustomerUtterance": f"<latest_utterance>{st.session_state.intent_customer_utterance}</latest_utterance>",
            "Intent": f"<intents>{st.session_state.intent_options}</intents>",
            "Ambiguity": f"<ambiguity_levels>{st.session_state.intent_ambiguity_level}</ambiguity_levels>",
            "Labelled?": None,
            "Comments": None,
        }

        pretty_json = json.dumps(benchmark, indent=2, ensure_ascii=False)
        with st.expander("JSON Output"):
            st.code(pretty_json, language="json", wrap_lines=True)
        st.download_button("📥 Download JSON", data=pretty_json, file_name="intent_classification.json",
                           mime="application/json", use_container_width=True)


def render_text_to_option() -> None:
    st.subheader("Fixed Instructions")
    with st.expander("Task Instructions"):
        st.markdown(TEXT_TO_OPTION_TASK_INSTRUCTIONS)
    with st.expander("K-Shot Examples"):
        st.code(TEXT_TO_OPTION_K_SHOT_EXAMPLES, language="xml")
    st.subheader("Per-Sample Section")
    render_text_to_option_form()


def render_text_to_option_form() -> None:
    st.text_input("Product Type", key="txt2_product_type")

    generation_mode = st.radio("Conversation history generation approach", ("Automatic", "Manual"), horizontal=True)

    if generation_mode == "Automatic":
        with st.expander("Generate Prompt"):
            with st.expander("Advanced"):
                examples_to_retrieve = st.number_input("Examples to retrieve", value=5)
                turns_to_generate = st.number_input("Turns to generate", value=3)

            examples = _auto_examples("Text2Options_100.jsonl", "ConversationHistory", int(examples_to_retrieve),
                                      "ProductType")
            add_auto_turn_fragment(st.session_state.txt2_product_type, "COMPASS", examples, int(turns_to_generate))
    else:
        init_state()
        add_manual_turn_fragment()

    st.text_input("Question", key="txt2_question")
    st.text_area("Options", key="txt2_options")
    st.text_input("Input", key="txt2_input")
    st.selectbox("Output Class", TEXT_TO_OPTION_OUTPUT_CLASS, key="txt2_output_class")
    st.number_input("Output Class Index", value=0, key="txt2_output_class_index")

    if st.button("Generate Text2Options JSON", use_container_width=True):
        synthetic_conv_key = "compass_synthetic_conversation"
        conversation_history = (
                st.session_state.get(synthetic_conv_key)
                or "\n".join(
            f"Customer: {c['user_input']}\nCOMPASS: {c['assistant_output']}" for c in
            st.session_state.get('chat_history', [])
        )
        )

        product_details = {
            "ProductType": f"<attributes>{st.session_state.get('txt2_product_type', '')}</attributes>",
            "ConversationHistory": f"<history>{conversation_history}</history>",
            "Question": f"<last_chatbot_question>{st.session_state.get('txt2_question', '')}</last_chatbot_question>",
            "Options": f"<question_classes>{st.session_state.get('txt2_options', '').strip().splitlines()}</question_classes>",
            "Input": f"<cust_query>{st.session_state.get('txt2_input', '')}</cust_query>",
            "OutputClass": st.session_state.get("txt2_output_class", ""),
            "OutputClassIndex": st.session_state.get("txt2_output_class_index", -1)
        }

        pretty_json = json.dumps(product_details, indent=2, ensure_ascii=False)
        with st.expander("JSON Output"):
            st.code(pretty_json, language="json", wrap_lines=True)

        st.download_button("📥 Download JSON", data=pretty_json, file_name="product_details.json",
                           mime="application/json", use_container_width=True)
