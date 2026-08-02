import { FileText, Upload } from "lucide-react";
import UploadBox from "./UploadBox";

function Sidebar() {
  return (
    <div className="w-72 border-r border-slate-800 bg-slate-900 p-6">
      <h1 className="mb-8 text-2xl font-bold text-blue-400">
        📚 DocMind AI
      </h1>

      <UploadBox />

      <div className="space-y-2">
      </div>
    </div>
  );
}

export default Sidebar;