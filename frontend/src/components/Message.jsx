function Message({ sender, text }) {
  const isUser = sender === "user";

  return (
    <div className={`mb-6 flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-2xl rounded-xl px-5 py-4 ${
          isUser
            ? "bg-blue-600"
            : "bg-slate-800"
        }`}
      >
        {text}
      </div>
    </div>
  );
}

export default Message;