
function Message({ sender, text, image }) {
  const isUser = sender === "user";

  // Backend image URL
const imageUrl = image
  ? `http://127.0.0.1:8000/chat-images/${image.image_path.split(/[\\/]/).pop()}`
  : null;

  return (
    <div className={`mb-6 flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-2xl rounded-xl px-5 py-4 ${
          isUser
            ? "bg-blue-600"
            : "bg-slate-800"
        }`}
      >

        {imageUrl && (
          <img
            src={imageUrl}
            alt="Uploaded attachment"
            className="mb-3 max-h-64 max-w-full rounded-lg object-contain"
          />
        )}

        {text && <p className="whitespace-pre-wrap">{text}</p>}

      </div>
    </div>
  );
}

export default Message;
