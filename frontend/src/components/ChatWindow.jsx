import ChatInput from "./ChatInput";
import Message from "./Message";

function ChatWindow() {
  return (
    <div className="flex flex-1 flex-col">
      <div className="flex-1 overflow-y-auto p-8">
        <Message
          sender="user"
          text="What is a matrix?"
        />

        <Message
          sender="bot"
          text="A matrix is an ordered rectangular array of numbers arranged in rows and columns."
        />
      </div>

      <ChatInput />
    </div>
  );
}

export default ChatWindow;