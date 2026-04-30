import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.llms import Tongyi
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 加载 API Key
load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")

# ── 页面设置 ──
st.set_page_config(page_title="智能文档问答", page_icon="📄")
st.title("📄 智能文档问答系统")
st.caption("上传 PDF，用自然语言提问，AI 回答并标注来源页码")

# ── 上传文件 ──
uploaded_file = st.file_uploader("上传你的 PDF 文件", type="pdf")

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("正在读取并分析文档，请稍候..."):

        # 1. 读取 PDF
        loader = PyMuPDFLoader(tmp_path)
        documents = loader.load()

        # 2. 切块
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)

        # 3. 向量化存入 FAISS
        embeddings = DashScopeEmbeddings(
            model="text-embedding-v2",
            dashscope_api_key=api_key
        )
        vectorstore = FAISS.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        # 4. 构建新版问答链
        llm = Tongyi(
            model_name="qwen-turbo",
            dashscope_api_key=api_key,
            temperature=0.1
        )

        prompt = PromptTemplate.from_template("""
你是一个文档问答助手，根据以下文档内容回答问题。
如果文档中没有相关信息，请直接说"文档中未找到相关内容"，不要编造答案。

文档内容：
{context}

问题：{question}

回答：""")

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        qa_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    st.success(f"文档加载完成，共 {len(chunks)} 个片段 ✅")

    # ── 问答区域 ──
    st.divider()
    question = st.text_input("💬 请输入你的问题：", placeholder="例如：这份文档的主要内容是什么？")

    if question:
        with st.spinner("AI 思考中..."):
            answer = qa_chain.invoke(question)
            # 单独获取来源文档
            source_docs = retriever.invoke(question)

        # 显示回答
        st.markdown("### 🤖 回答")
        st.write(answer)

        # 显示来源页码
        st.markdown("### 📌 参考来源")
        seen_pages = []
        for doc in source_docs:
            page = doc.metadata.get("page", 0) + 1
            if page not in seen_pages:
                seen_pages.append(page)
                with st.expander(f"第 {page} 页"):
                    st.write(doc.page_content)