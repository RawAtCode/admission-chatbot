
import os
import time
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from PyPDF2 import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://admission-chatbot.vercel.app",
        "https://ggsipu-admission-chatbot.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

PDF_FOLDER = "./pdfs"
FAISS_INDEX_PATH = "./faiss_index"

def load_pdfs():
    """ Load and process PDFs from the local folder """
    text = ""
    
    if not os.path.exists(PDF_FOLDER):
        print(f"⚠️ Warning: {PDF_FOLDER} does not exist. No PDFs loaded.")
        return ""

    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]

    if not pdf_files:
        print("⚠️ Warning: No PDF files found.")
        return ""

    for pdf_file in pdf_files:
        pdf_reader = PdfReader(os.path.join(PDF_FOLDER, pdf_file))
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=400,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return text_splitter.split_text(text)

def create_vector_store():
    """ Create FAISS vector store """
    try:
        raw_text = load_pdfs()
        if not raw_text:
            print("⚠️ No text extracted from PDFs. Skipping FAISS creation.")
            return

        text_chunks = get_text_chunks(raw_text)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        os.makedirs(FAISS_INDEX_PATH, exist_ok=True)

        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local(FAISS_INDEX_PATH)
        print(f"✅ FAISS index created successfully at {FAISS_INDEX_PATH}!")

    except Exception as e:
        print(f"❌ Error creating FAISS index: {e}")

print("⏳ Creating FAISS vector store...")
create_vector_store()
time.sleep(3)

class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


def get_answer(user_question):
    """Retrieve relevant documents and generate an answer using Gemini."""
    try:
        print("🔍 Loading FAISS index...")

        if not os.path.exists(f"{FAISS_INDEX_PATH}/index.faiss"):
            return "The admission database is still initializing. Please try again shortly."

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        new_db = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = new_db.similarity_search(user_question, k=8)

        print("\n========== RETRIEVED DOCUMENTS ==========")

        for i, doc in enumerate(docs, 1):
            print(f"\n--- Document {i} ---")
            print(doc.page_content[:1500])

        print("\n=========================================\n")

        if not docs:
            return "Refer to the official admission brochure for accurate details. Official contact email: pro@ipu.ac.in"

        context = "\n\n".join(doc.page_content for doc in docs)

        prompt_template = """
You are an AI assistant specialized in GGSIPU admissions.

Answer the user's question strictly using the provided PDF context.
Do not invent information or make assumptions.
Use clear, structured Markdown.

If the answer is not available in the context, respond:
"Refer to the official admission brochure for accurate details."
Official contact email: pro@ipu.ac.in

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        formatted_prompt = prompt.format(
            context=context,
            question=user_question
        )

        # Initialize Gemini BEFORE invoking it.
        model = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            timeout=60,
            max_retries=3
        )

        print("🤖 Sending request to Gemini...")
        response = model.invoke(formatted_prompt)

        print("========== GEMINI DEBUG ==========")
        print("Response type:", type(response))
        print("Response content:", repr(response.content))
        print("Additional kwargs:", repr(response.additional_kwargs))
        print("Response metadata:", repr(response.response_metadata))
        print("==================================")

        answer = response.content

        if isinstance(answer, str) and answer.strip():
            return answer.strip()

        if isinstance(answer, list):
            text_parts = [
                item.get("text", "")
                for item in answer
                if isinstance(item, dict)
            ]
            answer = "\n".join(text_parts).strip()

            if answer:
                return answer

        print("The model returned an empty or unexpected response.")
        return "The assistant could not generate an answer. Please try again."

    except Exception:
        logging.exception("Admission question processing failed")
        return "The admission assistant is temporarily unavailable. Please try again shortly."


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """ API endpoint to get answers from the AI model """
    answer = get_answer(request.question)
    return {"answer": answer}

if __name__ == "__main__":
    print("🚀 Starting FastAPI server...")
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting FastAPI server on port {port}...")
    uvicorn.run("main:app", host="0.0.0.0", port=port)

