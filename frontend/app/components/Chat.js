"use client";

import { useState } from "react";
import axios from "axios";
import { marked } from "marked";
import DOMPurify from "dompurify";
import Header from "./Header";
import Footer from "./Footer";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

  const askQuestion = async (query) => {
    if (!query.trim()) return;
    setLoading(true);
    setResponse("");

    try {
      const res = await axios.post(`${BACKEND_URL}/ask`, { question: query });
      setResponse(res.data.answer || "No response received.");
    } catch (error) {
      console.error("Error fetching response:", error);
      setResponse("Failed to get a response. Try again!");
    }

    setLoading(false);
  };

  const handleFAQClick = (faq) => {
    setQuestion(faq);
    window.scrollTo({ top: 0, behavior: "smooth" });
    askQuestion(faq);
  };

  return (
    <div className="app-body">
      <Header />

      {/* Main Content */}
      <div className="container">
        <div className="container-heading">
          <h1 className="text-3xl md:text-4xl font-bold text-center">GGSIPU Admission Chatbot</h1>
          <p className="text-gray-700 text-center mt-2 max-w-2xl mx-auto text-sm md:text-base">
            Ask me anything about admission queries. I'm here to assist you!
          </p>
        </div>

        {/* Input Section */}
        <div className="input-container w-full md:w-4/5 lg:w-3/5 mx-auto">
          <input
            type="text"
            id="query-field"
            className="input-field w-full p-3 md:p-4 text-sm md:text-base"
            placeholder="How may I help you?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && askQuestion(question)}
          />
          <button
            onClick={() => askQuestion(question)}
            className="ask-button w-full p-3 md:p-4 text-sm md:text-base"
            disabled={loading}
          >
            {loading ? "Retrieving Info..." : "Ask"}
          </button>
        </div>

        {/* Response Section */}
        {response && (
          <div className="response-container w-full md:w-4/5 lg:w-3/5 mx-auto mt-6">
            <div
              className="response-content"
              dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(marked(response)) }}
            />
          </div>
        )}

        {/* FAQ Section */}
        <div className="response-container w-full md:w-4/5 lg:w-3/5 mx-auto mt-6">
          <h2 className="text-xl font-bold text-gray-800 mb-3 text-center">
            Frequently Asked Questions
          </h2>
          <div className="w-100 border-t border-gray-300 opacity-70 mb-5"></div>
          <ul className="space-y-3 text-gray-650">
            {[
              "What are the CET examination dates?",
              "How will the seats be allotted in GGSIPU online counselling?",
              "What is the fee for MCA?",
              "What is the last date for admissions?",
              "What is the fee structure for B.Tech?",
            ].map((faq, index) => (
              <li
                key={index}
                className="p-3 bg-white rounded-lg shadow-sm border border-gray-300 cursor-pointer hover:bg-gray-100 transition text-sm md:text-base whitespace-normal break-words"
                onClick={() => handleFAQClick(faq)}
              >
                <strong>‣ {faq}</strong>
              </li>
            ))}
          </ul>
        </div>

        
      </div>

      <Footer />
    </div>
  );
}