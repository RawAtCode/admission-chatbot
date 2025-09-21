from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import time
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://admission-chatbot.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    """ Split text into chunks for embedding """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
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
    question: str

def get_answer(user_question):
    """ Retrieve answer from FAISS index """
    try:
        print("🔍 Checking FAISS index file...")
        
        if not os.path.exists(f"{FAISS_INDEX_PATH}/index.faiss"):
            print("❌ FAISS index file not found! Ensure it is created before querying.")
            return "Apologies! The system is still initializing. Please try again in a few minutes."

        print("✅ FAISS index found! Loading FAISS...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        try:
            new_db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
            print("✅ FAISS index loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading FAISS: {e}")
            return f"❌ Error loading FAISS index: {e}"

        print("🔍 Searching similar documents...")
        docs = new_db.similarity_search(user_question)
        print(f"✅ Retrieved {len(docs)} similar docs")

        if not docs:
            print("⚠️ No relevant documents found.")
            return "Apologies! No relevant information found."

        print("🤖 Generating AI response...")
        model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.3)
        prompt_template = """
        You are an AI assistant specialized in answering queries about **GGSIPU Admissions**. Your responses must be **highly structured, well-formatted, and in clean Markdown** based strictly on the provided PDF documents.  

        # 🛑 **STRICT RULES:**  
        - **ONLY use information from the given PDFs**. Do NOT generate responses based on assumptions.  
        - **DO NOT** add greetings, disclaimers, or extra text.  
        - **DO NOT** start with anything except the direct answer.  
        - **FORMAT the response in clear, structured Markdown** as per the guidelines below.  

        # ✅ **MARKDOWN FORMAT GUIDELINES:**  
        - `#` → **Main Topics**  
        - `##` → **Subtopics**  
        - `###` → **Detailed Sections**  
        - `-` → **Bullet Points for clarity**  
        - **Bold** → **For highlighting key terms**  
        - Ensure **at least ONE blank line** between major sections for readability.  

        # 🚨 **MISSING INFORMATION HANDLING:**  
        If the answer is **not available in the PDFs**, respond with:  
        - **"Refer to the official admission brochure for accurate details."**  
        - **Official contact email:** `pro@ipu.ac.in`  
        - **DO NOT** guess, assume, or fabricate any information.  

        - **If the gemini model hits rate limit or is down, then display this message:** `Too many requests are being processed by the server currently. We appreciate your patience.` 

        ---

        # 📌 **CONTEXT (Extracted from PDFs):**  
        {context}  

        # 📌 **USER QUERY:**  
        {question}  

        # 📌 **STRUCTURED ANSWER:**  
        

        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        print("✅ AI Response Generated!")

        return response["output_text"]

    except Exception as e:
        print(f"❌ Error retrieving answer: {e}")
        return f"❌ Error: {e}"


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """ API endpoint to get answers from the AI model """
    answer = get_answer(request.question)
    return {"answer": answer}

if __name__ == "__main__":
    print("🚀 Starting FastAPI server...")
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting FastAPI server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)

