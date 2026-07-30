import { FileText, Upload } from "lucide-react";
import UploadBox from "./UploadBox";

function Sidebar() {
  return (
    <div className="w-72 border-r border-slate-800 bg-slate-900 p-6">
      <h1 className="mb-8 text-2xl font-bold text-blue-400">
        📚 DocMind AI
      </h1>

      <UploadBox />

      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wider text-slate-400">
        Uploaded Files
      </h2>

      <div className="space-y-2">
        <div className="flex items-center gap-2 rounded-lg bg-slate-800 p-3">
          <FileText size={18} />
          <span>Math.pdf</span>
        </div>

        <div className="flex items-center gap-2 rounded-lg bg-slate-800 p-3">
          <FileText size={18} />
          <span>Physics.pdf</span>
        </div>
      </div>
    </div>
  );
}

export default Sidebar;