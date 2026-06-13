### Team Name: ThinkSphere

# EduMind AI

## Learn Smarter. Study Better.

EduMind AI is an intelligent academic assistant designed to help students learn, revise, and prepare for examinations more efficiently. The platform allows users to upload academic documents such as lecture notes, textbooks, study materials, presentations, and reference documents, then interact with them using natural language queries.

By combining Retrieval-Augmented Generation (RAG), Vector Search, and Large Language Models, EduMind AI provides context-aware answers directly from uploaded study material instead of generating generic responses.

---

## Problem Statement

Students often struggle with:

* Searching through large volumes of notes and textbooks.
* Finding important exam questions.
* Creating revision notes quickly.
* Understanding complex academic concepts.
* Preparing structured answers for examinations.
* Revising multiple subjects efficiently before exams.

EduMind AI addresses these challenges by transforming static study materials into an interactive AI-powered learning assistant.

---

## Key Features

### 1. Topic Explanation

Students can ask questions about any topic from their uploaded documents and receive:

* Detailed explanations
* Definitions
* Examples
* Applications
* Important exam points

---

### 2. Exam Ready Answer Generator

Generates well-structured university-style answers suitable for writing directly in examinations.

Output includes:

* Introduction
* Main explanation
* Examples
* Conclusion
* Key exam points

---

### 3. Question Paper Solver

Designed specifically for solving previous-year examination questions.

Provides:

* Question understanding
* Complete solution
* Step-by-step explanation
* Marks-wise answer structure
* Important points for scoring better marks

---

### 4. Study Guide Generator

Automatically creates a complete revision guide from uploaded study material.

Includes:

* Topic overview
* Key concepts
* Important definitions
* Viva questions
* Exam tips
* Revision content

---

### 5. Important Questions Generator

Analyzes study material and generates probable examination questions such as:

* 2-Mark Questions
* 5-Mark Questions
* 10-Mark Questions
* Long Answer Questions
* Viva Questions
* Frequently expected questions

---

### 6. Notes Generator

Creates concise revision notes from uploaded academic content.

Provides:

* Topic summaries
* Important definitions
* Key concepts
* Important formulas
* Quick revision points

---

### 7. Multi-Document Support

Supports uploading multiple files simultaneously including:

* PDF Documents
* DOCX Files
* PPTX Presentations

The system combines knowledge from all uploaded documents to provide comprehensive answers.

---

### 8. Retrieval-Augmented Generation (RAG)

Instead of relying only on the language model, EduMind AI:

1. Extracts content from uploaded documents.
2. Splits content into meaningful chunks.
3. Generates embeddings.
4. Stores embeddings in a FAISS Vector Database.
5. Retrieves relevant information during queries.
6. Generates context-aware responses.

This improves answer accuracy and reduces hallucinations.

---

### 9. Source Tracking

Every response is accompanied by retrieved source sections, allowing students to verify information directly from their uploaded study materials.

---

### 10. Query History

Maintains a recent query history to help users revisit previous interactions.

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI & Machine Learning

* Google Gemini
* LangChain
* Retrieval-Augmented Generation (RAG)

### Vector Database

* FAISS (Facebook AI Similarity Search)

### Document Processing

* PyPDF2
* python-docx
* python-pptx

---

## Project Architecture

1. Upload Documents
2. Extract Text
3. Create Chunks
4. Generate Embeddings
5. Store in FAISS Vector Database
6. Retrieve Relevant Context
7. Generate AI Response
8. Display Answer with Sources

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/EduMind-AI.git
cd EduMind-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

Run the application:

```bash
streamlit run app.py
```

---

## Future Enhancements

* OCR support for handwritten notes
* Voice-based interaction
* Automatic quiz generation
* Flashcard generation
* Personalized study recommendations
* Academic performance analytics
* Multi-language support

---

## Team ThinkSphere

EduMind AI was developed by Team ThinkSphere with the vision of making learning more interactive, efficient, and accessible through Artificial Intelligence.

### Motto

**Learn Smarter. Study Better.**
