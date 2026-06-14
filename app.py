import re
import time
import streamlit as st
from groq import RateLimitError, BadRequestError

from processors.pdf import extract_pdf_text
from processors.doc import extract_docx_text
from processors.ppt import extract_ppt_text

from rag.chunker import create_chunks
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store
from rag.retriever import retrieve_docs
from rag.qa_engine import get_llm


# -------------------------
# Streamlit Config
# -------------------------

st.set_page_config(
    page_title="EduMind AI",
    layout="wide"
)

# -------------------------
# Session State
# -------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

# -------------------------
# Cache Functions
# -------------------------

@st.cache_resource(show_spinner=False)
def load_embeddings():
    return get_embeddings()


@st.cache_resource(show_spinner=False)
def build_vector_db(chunks, metadata):

    embeddings = load_embeddings()

    return create_vector_store(
        list(chunks),
        embeddings,
        list(metadata)
    )


# -------------------------
# Context Cleaner
# -------------------------

def clean_context(text):
    text = text.encode("utf-8", errors="ignore").decode("utf-8")
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🎓 EduMind Dashboard")

st.sidebar.markdown("---")

# -------------------------
# Stats Section
# -------------------------

st.sidebar.subheader("📊 Session Stats")

col_a, col_b = st.sidebar.columns(2)

with col_a:
    st.metric("Queries", st.session_state.total_queries)

with col_b:
    st.metric("Bookmarks", len(st.session_state.bookmarks))

st.sidebar.markdown("---")

# -------------------------
# Recent Queries Section
# -------------------------

st.sidebar.subheader("🕘 Recent Queries")

if len(st.session_state.history) == 0:
    st.sidebar.caption("No queries yet")

else:
    for item in reversed(st.session_state.history[-5:]):

        with st.sidebar.expander(
            f"🔹 {item['question'][:35]}..."
            if len(item['question']) > 35
            else f"🔹 {item['question']}"
        ):
            st.caption(f"Subject: {item.get('subject', 'General')}")
            st.caption(f"Mode: {item['mode']}")
            st.write(item['answer'][:300] + "..." if len(item['answer']) > 300 else item['answer'])

st.sidebar.markdown("---")

# -------------------------
# Bookmarks Section
# -------------------------

st.sidebar.subheader("🔖 Bookmarks")

if len(st.session_state.bookmarks) == 0:
    st.sidebar.caption("No bookmarks yet")

else:

    if st.sidebar.button("🗑️ Clear All Bookmarks"):
        st.session_state.bookmarks = []
        st.rerun()

    for i, bm in enumerate(st.session_state.bookmarks):

        with st.sidebar.expander(
            f"📌 {bm['question'][:35]}..."
            if len(bm['question']) > 35
            else f"📌 {bm['question']}"
        ):
            st.caption(f"Subject: {bm.get('subject', 'General')}")
            st.caption(f"Mode: {bm['mode']}")
            st.write(bm['answer'][:300] + "..." if len(bm['answer']) > 300 else bm['answer'])

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "⬇️ Download",
                    bm['answer'],
                    file_name=f"bookmark_{i+1}.txt",
                    mime="text/plain",
                    key=f"download_bm_{i}"
                )

            with col2:
                if st.button(
                    "🗑️ Remove",
                    key=f"remove_bookmark_{i}"
                ):
                    st.session_state.bookmarks.pop(i)
                    st.rerun()

st.sidebar.markdown("---")

# -------------------------
# Clear History Button
# -------------------------

st.sidebar.subheader("⚙️ Session Controls")

if st.sidebar.button("🧹 Clear Query History"):
    st.session_state.history = []
    st.session_state.total_queries = 0
    st.rerun()

if st.sidebar.button("🔄 Reset Everything"):
    st.session_state.history = []
    st.session_state.bookmarks = []
    st.session_state.total_queries = 0
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("EduMind AI — Learn Smarter. Study Better.")

# -------------------------
# MAIN UI
# -------------------------

st.markdown(
    """
    <h1 style='text-align:center;'>
        EduMind AI
    </h1>

    <h4 style='text-align:center;color:gray;'>
        Learn Smarter. Study Better.
    </h4>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Upload Academic Documents",
    type=["pdf", "docx", "pptx"],
    accept_multiple_files=True
)

# -------------------------
# Main Logic
# -------------------------

if uploaded_files:

    all_chunks = []
    all_metadata = []

    for file in uploaded_files:

        if file.name.endswith(".pdf"):
            text = extract_pdf_text(file)

        elif file.name.endswith(".docx"):
            text = extract_docx_text(file)

        elif file.name.endswith(".pptx"):
            text = extract_ppt_text(file)

        else:
            text = ""

        filename = file.name.lower()

        if re.search(r'\bdbms\b', filename):
            subject = "DBMS"

        elif re.search(r'\bos\b', filename):
            subject = "Operating Systems"

        elif re.search(r'\bcn\b', filename):
            subject = "Computer Networks"

        elif re.search(r'\bjava\b', filename):
            subject = "Java"

        elif re.search(r'\bpython\b', filename):
            subject = "Python"

        else:
            subject = "General"

        chunks = create_chunks(text)

        for chunk in chunks:

            all_chunks.append(chunk)

            all_metadata.append(
                {
                    "source": file.name,
                    "subject": subject
                }
            )

    if len(all_chunks) == 0:
        st.error("No text extracted from uploaded files.")
        st.stop()

    db = build_vector_db(
        tuple(all_chunks),
        tuple(all_metadata)
    )

    llm = get_llm()

    # -------------------------
    # Uploaded Files Info
    # -------------------------

    with st.sidebar:

        st.markdown("---")
        st.subheader("📁 Uploaded Files")

        for file in uploaded_files:

            filename = file.name.lower()

            if re.search(r'\bos\b', filename):
                icon = "🖥️"
            elif re.search(r'\bdbms\b', filename):
                icon = "🗄️"
            elif re.search(r'\bcn\b', filename):
                icon = "🌐"
            elif re.search(r'\bjava\b', filename):
                icon = "☕"
            elif re.search(r'\bpython\b', filename):
                icon = "🐍"
            else:
                icon = "📄"

            st.write(f"{icon} {file.name}")

        st.metric("Total Chunks", len(all_chunks))
        st.success("✅ Knowledge Base Ready")

    # -------------------------
    # Mode Selection
    # -------------------------

    st.markdown("### 🎯 Select Mode")

    mode = st.selectbox(
        "Select Mode",
        [
            "Topic Explanation (Learn a concept in detail)",
            "Exam Ready Answer (Generate a structured exam answer)",
            "Question Paper Solver (Solve previous year questions)",
            "Study Guide Generator (Create a complete revision guide)",
            "Important Questions Generator (Generate probable exam questions)",
            "Generate Notes (Create concise revision notes)"
        ],
        label_visibility="collapsed"
    )

    # -------------------------
    # Query Input
    # -------------------------

    note_modes = [
        "Study Guide Generator (Create a complete revision guide)",
        "Important Questions Generator (Generate probable exam questions)",
        "Generate Notes (Create concise revision notes)"
    ]

    st.markdown("### 💬 Your Query")

    if mode in note_modes:

        query = st.text_input(
            "Optional Topic Filter",
            placeholder="Leave blank to use all uploaded documents"
        )

        generate_btn = st.button("⚡ Generate", use_container_width=True)

    else:

        query = st.text_input(
            "Ask a Question",
            placeholder="Example: Explain the LRU page replacement algorithm"
        )

        generate_btn = bool(query)

    # -------------------------
    # Generation Logic
    # -------------------------

    if generate_btn:

        docs = []

        MAX_CONTEXT_CHARS = 1500

        if mode in note_modes:

            if query.strip():

                filtered_chunks = [
                    chunk for chunk in all_chunks
                    if query.lower() in chunk.lower()
                ]

                context = "\n\n".join(
                    filtered_chunks if filtered_chunks else all_chunks[:5]
                )

            else:
                context = "\n\n".join(all_chunks[:5])

            context = context[:MAX_CONTEXT_CHARS]
            context = clean_context(context)

        else:

            if not query:
                st.warning("Please enter a question")
                st.stop()

            docs = retrieve_docs(db, query)

            context = "\n\n".join([doc.page_content for doc in docs])
            context = context[:MAX_CONTEXT_CHARS]
            context = clean_context(context)

        # -------------------------
        # PROMPT
        # -------------------------

        if mode == "Topic Explanation (Learn a concept in detail)":

            prompt = f"""
Use ONLY the provided context.

Context:
{context}

Question:
{query}

Provide:
1. Definition
2. Detailed Explanation
3. Examples
4. Applications
5. Important Exam Points
"""

        elif mode == "Exam Ready Answer (Generate a structured exam answer)":

            prompt = f"""
Generate a university exam-ready answer.

Use ONLY the provided context.

Context:
{context}

Question:
{query}

Format:
1. Introduction
2. Main Answer
3. Examples
4. Conclusion
5. Important Exam Points
"""

        elif mode == "Question Paper Solver (Solve previous year questions)":

            prompt = f"""
You are a university exam expert.

Use ONLY the provided context.

Context:
{context}

Question:
{query}

Provide:
1. Question Understanding
2. Complete Solution
3. Step-by-step Explanation
4. Marks-wise Answer Structure
5. Important Points
"""

        elif mode == "Study Guide Generator (Create a complete revision guide)":

            prompt = f"""
Create a complete study guide.

Use ONLY the provided context.

Context:
{context}

Topic:
{query}

Generate:
1. Topic Overview
2. Key Concepts
3. Important Definitions
4. Important Questions
5. Viva Questions
6. Exam Tips
"""

        elif mode == "Important Questions Generator (Generate probable exam questions)":

            prompt = f"""
Analyze the study material.

Use ONLY the provided context.

Context:
{context}

Topic:
{query}

Generate:
1. 2-Mark Questions
2. 5-Mark Questions
3. 10-Mark Questions
4. Long Answer Questions
5. Viva Questions
6. Most Important Questions
"""

        else:

            prompt = f"""
Generate concise revision notes.

Use ONLY the provided context.

Context:
{context}

Topic:
{query}

Provide:
1. Topic Summary
2. Important Definitions
3. Key Concepts
4. Important Formulas
5. Exam Points
6. One-Page Quick Revision Notes
"""

        # -------------------------
        # LLM CALL
        # -------------------------

        max_retries = 3
        answer = None

        for attempt in range(max_retries):

            try:

                with st.spinner("🤖 Generating answer..."):
                    response = llm.invoke(prompt)
                    answer = response.content

                break

            except RateLimitError:

                if attempt < max_retries - 1:

                    with st.spinner(
                        f"⏳ Rate limit hit. Waiting 30 seconds before retry {attempt + 1} of {max_retries - 1}..."
                    ):
                        time.sleep(30)

                else:

                    st.warning(
                        """
                        ⚠️ **Rate limit reached.**

                        Please try one of the following:
                        - Wait **1-2 minutes** and click Generate again
                        - Upload a **smaller document**
                        - Try a **shorter or simpler question**

                        This is a free-tier API limit and resets automatically.
                        """
                    )
                    st.stop()

            except BadRequestError as e:

                st.error(f"⚠️ Bad request error: {str(e)}")
                st.stop()

        # -------------------------
        # OUTPUT
        # -------------------------

        if answer:

            detected_subject = all_metadata[0]["subject"] if all_metadata else "General"

            st.session_state.total_queries += 1

            st.session_state.history.append(
                {
                    "question": query if query else "Generated Content",
                    "mode": mode,
                    "answer": answer,
                    "subject": detected_subject
                }
            )

            st.markdown("---")

            # Subject Badge + Answer Header
            st.markdown(
                f"""
                <div style='background:#1e1e2e;padding:16px;border-radius:10px;margin-bottom:10px;'>
                    <span style='background:#4A90D9;color:white;padding:4px 12px;border-radius:20px;font-size:14px;'>
                        {detected_subject}
                    </span>
                    <h3 style='color:white;margin-top:10px;'>
                        {query if query else "Generated Content"}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(answer)

            st.markdown("---")

            # Action Buttons
            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    "⬇️ Download Answer",
                    answer,
                    file_name="academic_answer.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with col2:

                already_bookmarked = any(
                    bm["question"] == (query if query else "Generated Content")
                    and bm["answer"] == answer
                    for bm in st.session_state.bookmarks
                )

                if already_bookmarked:
                    st.info("✅ Bookmarked")

                else:
                    if st.button(
                        "🔖 Bookmark",
                        use_container_width=True
                    ):
                        st.session_state.bookmarks.append(
                            {
                                "question": query if query else "Generated Content",
                                "mode": mode,
                                "answer": answer,
                                "subject": detected_subject
                            }
                        )
                        st.rerun()

            with col3:
                if st.button(
                    "🧹 Clear Answer",
                    use_container_width=True
                ):
                    st.rerun()

            if docs:

                st.markdown("---")
                st.subheader("📚 Sources Used")

                for i, doc in enumerate(docs):

                    source_file = doc.metadata.get("source", "Unknown File")
                    subject = doc.metadata.get("subject", "General")

                    with st.expander(
                        f"Source {i+1} | {subject} | {source_file}"
                    ):
                        st.write(doc.page_content)