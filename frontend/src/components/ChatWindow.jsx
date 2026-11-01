
import { useState } from "react";
import ChatInput from "./ChatInput";
import Message from "./Message";
import api from "../services/api";

function ChatWindow() {
  const [messages, setMessages] = useState([]);

  // Remember the currently active image
  const [activeImageId, setActiveImageId] = useState(null);

  const sendQuestion = async (question, imageData = null) => {

    const userText = question.trim();

    // If a new image is uploaded, remember its ID
    if (imageData?.image_id) {
      setActiveImageId(imageData.image_id);
    }

    // Use the new image ID or the previously uploaded image ID
    const currentImageId = imageData?.image_id || activeImageId;

    // Display user message
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: userText || "Describe this image.",
        image: imageData,
      },
    ]);

    try {
      const response = await api.post("/query", {
        question: userText,
        image_id: currentImageId,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response.data.answer,
        },
      ]);

    } catch (err) {
      console.error("Query error:", err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text:
            err.response?.data?.detail ||
            "Something went wrong. Please try again.",
        },
      ]);
    }
  };

  return (
    <div className="flex flex-1 flex-col">

      <div className="flex-1 overflow-y-auto p-8 space-y-4">

        {messages.length === 0 && (
          <div className="text-center text-slate-500 mt-20">
            Upload a PDF or an image and ask your first question.
          </div>
        )}

        {messages.map((msg, index) => (
          <Message
            key={index}
            sender={msg.sender}
            text={msg.text}
            image={msg.image}
          />
        ))}

      </div>

      <ChatInput onSend={sendQuestion} />

    </div>
  );
}

export default ChatWindow;
