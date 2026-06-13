# EduMind AI

### Learn Smarter. Study Better.

EduMind AI is an AI-powered academic assistant that helps students learn from their own study materials. By combining Retrieval-Augmented Generation (RAG), vector search, and Large Language Models, EduMind AI can analyze uploaded documents and generate accurate, context-aware academic responses.

---

## Problem Statement

Students often study from multiple sources such as lecture notes, textbooks, PowerPoint presentations, and previous year question papers. Finding relevant information quickly and preparing for examinations can be time-consuming.

EduMind AI addresses this challenge by transforming uploaded academic resources into an intelligent knowledge base that can answer questions, generate study materials, and assist with exam preparation.

---

## Key Features

### Topic Explanation

Generate detailed explanations for academic concepts using uploaded study materials.

### Exam Ready Answer

Create structured university-style answers suitable for direct exam writing.

### Question Paper Solver

Solve previous year questions with detailed explanations and marks-wise answer formatting.

### Study Guide Generator

Generate complete revision guides covering important concepts, definitions, and exam-focused content.

### Important Questions Generator

Automatically identify and generate probable examination questions.

### Notes Generator

Create concise revision notes and quick-reference study material.

### Multi-Document Knowledge Base

Combine multiple PDFs, DOCX files, and PPT presentations into a single searchable academic knowledge base.

### Source-Based Responses

Answers are generated using only the uploaded documents, ensuring contextual relevance.

---

## Technology Stack

### Frontend

* Streamlit

### AI & NLP

* Google Gemini
* LangChain

### Retrieval-Augmented Generation (RAG)

* Text Chunking
* Embeddings
* Semantic Search

### Vector Database

* FAISS

### Document Processing

* PDF Processing
* DOCX Processing
* PPTX Processing

---

## System Architecture

User Uploads Documents
↓
Document Processing
(PDF / DOCX / PPTX)
↓
Text Extraction
↓
Text Chunking
↓
Embedding Generation
↓
FAISS Vector Database
↓
Semantic Retrieval
↓
Google Gemini
↓
Generated Academic Response

---

## Supported File Formats

* PDF
* DOCX
* PPTX

---

## Example Academic Scenarios

### Scenario 1

Upload DBMS notes and ask:

> Explain Database Normalization with examples.

### Scenario 2

Upload Operating Systems material and generate:

> Important 10-mark examination questions.

### Scenario 3

Upload Computer Networks notes and request:

> Complete study guide for TCP/IP Protocol.

### Scenario 4

Upload previous year question papers and generate:

> Exam-ready answers with proper structure.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/SnehaM-96/EduMind-AI.git
cd EduMind-AI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## API Configuration

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Live Demo

```text
https://sneham-96-edumind-ai-app-osvvz2.streamlit.app/
```

---

## Team

### ThinkSphere

---

## Future Enhancements

* OCR support for handwritten notes
* Subject-wise analytics dashboard
* Flashcard generation
* Quiz generation
* Voice-based academic assistant
* Performance tracking and learning insights

---

## License

This project is developed for educational and academic purposes.
