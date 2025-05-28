import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# 環境変数を読み込む
load_dotenv()

# OpenAI APIキーを環境変数から取得
api_key = os.getenv("OPENAI_API_KEY")

# タイトルと説明
st.title("🧠 専門家LLMアプリ")
st.write("このアプリでは、質問に対して選択した専門家になりきったLLMが回答します。")
st.write("以下から専門家を選び、質問を入力してください。")

# 専門家の選択肢
expert_options = {
    "マーケティングの専門家": "あなたはマーケティング戦略の専門家です。ユーザーの課題に対して実践的かつ創造的なアドバイスを提供してください。",
    "栄養学の専門家": "あなたは栄養学の専門家です。ユーザーの健康に関する疑問に対して、科学的根拠に基づいた回答を行ってください。"
}
expert_choice = st.radio("専門家を選んでください：", list(expert_options.keys()))

# ユーザー入力フォーム
user_input = st.text_input("質問を入力してください:")

# 回答生成関数
def get_response_from_llm(question: str, expert_type: str) -> str:
    system_message = expert_options[expert_type]

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}")
    ])

    llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo")
    chain = prompt | llm
    return chain.invoke({"input": question})

# 実行処理
if user_input:
    with st.spinner("考え中..."):
        response = get_response_from_llm(user_input, expert_choice)
        st.success("回答：")
        st.write(response.content)
