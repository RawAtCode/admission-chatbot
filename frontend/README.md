# **AI Chatbot - Admission Inquiry Assistant** 🚀  

## **📌 Project Overview**  
This is an **AI-powered chatbot** designed to assist with **admission inquiries**. It leverages **FastAPI**, **LangChain**, and **Google Generative AI** to answer queries based on **PDF documents** stored in a vector database (**FAISS**). The frontend is built using **Next.js** and **Tailwind CSS**.  

---

## **📂 Project Structure**  

```
ai-chatbot/
├── backend/                 # FastAPI backend  
│   ├── main.py              # Core API logic  
│   ├── pdfs/                # PDF documents for knowledge base  
│   ├── faiss_index/         # FAISS vector store (ignored in Git)  
│   ├── service.json         # Google API service credentials  
│   ├── requirements.txt     # Backend dependencies  
│   └── .gitignore  
└── frontend/                # Next.js frontend  
    ├── app/                 # Frontend components and pages  
    │   ├── components/      # Header, Footer, Chat UI  
    ├── public/              # Static assets (e.g., IPU logo)  
    ├── tailwind.config.mjs  # Tailwind CSS config  
    ├── package.json         # Frontend dependencies  
    ├── next.config.mjs      # Next.js configuration  
    └── .gitignore  
```

---

## **🛠️ Tech Stack**  

### **Backend (FastAPI)**
- **FastAPI** – High-performance API framework  
- **LangChain** – Manages LLM-powered responses  
- **Google Generative AI** – Provides intelligent chatbot responses  
- **FAISS** – Vector database for storing and retrieving document embeddings  
- **PyPDF2** – Extracts text from PDFs  

### **Frontend (Next.js)**
- **Next.js** – React-based frontend framework  
- **Tailwind CSS** – Modern CSS framework for styling  

---

## **🚀 Setup & Installation**  

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Yash18Singh/ai-chatbot.git
cd ai-chatbot
```

### **2️⃣ Backend Setup**
#### **📌 Install dependencies**
```sh
cd backend
pip install -r requirements.txt
```

#### **📌 Set up `.env` file**
Create a `.env` file inside the `backend/` folder:
```
GOOGLE_API_KEY=your_google_api_key_here
```

#### **📌 Start the FastAPI server**
```sh
uvicorn main:app --reload
```
The backend should now be running at **`http://127.0.0.1:8000/`** 🚀  

---

### **3️⃣ Frontend Setup**
#### **📌 Install dependencies**
```sh
cd frontend
npm install
```

#### **📌 Start the Next.js frontend**
```sh
npm run dev
```
The frontend should now be running at **`http://localhost:3000/`** 🎉  

---

## **📌 Features**
✔️ **PDF-based Question Answering** – Queries are answered based on admission-related PDFs  
✔️ **FastAPI Backend** – High-performance API for quick responses  
✔️ **Vector Search (FAISS)** – Efficient information retrieval  
✔️ **Google Generative AI** – Smart and accurate chatbot responses  
✔️ **Modern UI (Next.js & Tailwind CSS)** – Clean and responsive frontend  

---

## **💡 Future Improvements**
🔹 Add support for **multiple document sources**  
🔹 Improve **response formatting**  
🔹 Implement **user authentication**  
🔹 Enhance **error handling**  

---

## **👨‍💻 Contributors**
- **Rawat** ([@rawatcode](https://github.com/rawatcode))  
- **Yash Singh** ([@Yash18Singh](https://github.com/Yash18Singh))  

---

## **📜 License**
This project is **open-source** and available under the **MIT License**.  

---

### **🚀 Happy Coding! 🎉**  
