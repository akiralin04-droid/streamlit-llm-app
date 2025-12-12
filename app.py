import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv()

st.set_page_config(page_title="専門家相談ツール", page_icon="🤖")


def ask_expert(user_text: str, selected_role: str) -> str:
    """入力テキストと選択した専門家タイプを基に回答する。"""
    role_prompts = {
        "A": "あなたはA領域の専門家です。専門的な視点で、具体的かつ実践的な提案を日本語で簡潔に伝えてください。",
        "B": "あなたはB領域の専門家です。リスクとメリットを整理し、根拠を添えて日本語で回答してください。",
    }
    system_prompt = role_prompts.get(selected_role, role_prompts["A"])

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text),
    ]
    response = llm.invoke(messages)
    return response.content


st.title("専門家相談ツール")
st.write(
    """
    入力フォームに相談内容を入力し、専門家タイプを選んで送信すると、
    専門家が回答します。
    """
)
st.info(
    "使い方: 専門家タイプを選択 → 相談内容を入力 → 「送信」ボタンを押下",
    icon="ℹ️",
)

if not os.getenv("OPENAI_API_KEY"):
    st.warning("環境変数 OPENAI_API_KEY を設定してください。", icon="⚠️")

experts = {
    "A: 戦略・企画系の専門家": "A",
    "B: データ分析・技術系の専門家": "B",
}

selected_label = st.radio("専門家の種類", list(experts.keys()))
selected_role = experts[selected_label]

user_text = st.text_area(
    "相談したい内容を入力してください",
    placeholder="例: 新規サービスのコンセプト検討について助言してください。",
    height=180,
)

if st.button("送信"):
    if not user_text.strip():
        st.error("相談内容を入力してください。")
    else:
        with st.spinner("専門家が回答を生成しています..."):
            answer = ask_expert(user_text, selected_role)
        st.success("回答が届きました。")
        st.write(answer)