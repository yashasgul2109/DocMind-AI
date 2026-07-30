import { Send } from "lucide-react";

function ChatInput() {
  return (
    <div className="border-t border-slate-800 bg-slate-900 p-5">
      <div className="flex items-center gap-3 rounded-xl bg-slate-800 p-3">
        <input
          type="text"
          placeholder="Ask anything..."
          className="flex-1 bg-transparent outline-none"
        />

        <button className="rounded-lg bg-blue-600 p-3 transition hover:bg-blue-700">
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}

export default ChatInput;