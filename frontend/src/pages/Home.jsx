import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";

function Home() {
  return (
    <div className="flex h-screen bg-slate-950 text-white">
      <Sidebar />
      <ChatWindow />
    </div>
  );
}

export default Home;