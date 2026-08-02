import { useState } from "react";
import ChatInput from "./ChatInput";
import Message from "./Message";
import api from "../services/api";

function ChatWindow() {
  const [messages, setMessages] = useState([]);

  const sendQuestion = async (question) => {
    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text: question,
      },
    ]);

    try {
      const response = await api.post("/query", {
        question,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response.data.answer,
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Something went wrong.",
        },
      ]);
    }
  };

  return (
    <div className="flex flex-1 flex-col">

      <div className="flex-1 overflow-y-auto p-8 space-y-4">

        {messages.length === 0 && (
          <div className="text-center text-slate-500 mt-20">
            Upload a PDF and ask your first question.
          </div>
        )}

        {messages.map((msg, index) => (
          <Message
            key={index}
            sender={msg.sender}
            text={msg.text}
          />
        ))}

      </div>

      <ChatInput onSend={sendQuestion} />

    </div>
  );
}

export default ChatWindow;