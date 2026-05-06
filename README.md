# 智能文档问答系统

基于 RAG（检索增强生成）架构开发的智能文档问答工具，支持上传 PDF 文件，用自然语言提问，AI 自动检索相关内容并生成回答，同时标注来源页码。

## 功能特点

- 支持 PDF 文档上传与解析
- 基于语义搜索的文档检索（FAISS 向量库）
- 自然语言提问，AI 生成精准回答
- 自动标注答案来源页码，可溯源
- 简洁易用的 Web 界面（Streamlit）

## 技术栈

| 模块 | 技术 |
|------|------|
| 文档解析 | PyMuPDF |
| 文本分块 | LangChain Text Splitters |
| 向量化 | 阿里云百炼 Embedding API |
| 向量存储 | FAISS |
| 大语言模型 | 通义千问 qwen-turbo |
| 链路编排 | LangChain LCEL |
| 前端界面 | Streamlit |

## 本地运行

**1. 克隆项目**
```bash
git clone https://github.com/pingguoli182-sys/doc-qa.git
cd doc-qa
```

**2. 安装依赖**
```bash
pip install langchain langchain-community langchain-text-splitters openai pymupdf faiss-cpu streamlit python-dotenv dashscope
```

**3. 配置 API Key**

在项目根目录新建 `.env` 文件：

**4. 启动应用**
```bash
python -m streamlit run app.py
```

打开浏览器访问 `http://localhost:8501`

## 使用方式

1. 上传 PDF 文件
2. 等待文档解析完成
3. 在输入框输入问题
4. 查看 AI 回答及来源页码

## 📸 项目截图

![上传文档](<Screen shots/Smart Q&A1.png>)
![上传文档](<Screen shots/Smart Q&A2.png>)
![上传文档](<Screen shots/Smart Q&A3.png>)
![上传文档](<Screen shots/Smart Q&A4.png>)

## 作者

李佳 · [github.com/pingguoli182-sys](https://github.com/pingguoli182-sys)