import { Upload, FileText } from "lucide-react";
import { useRef, useState } from "react";
import api from "../services/api";

function UploadBox() {
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleFile = async (selectedFile) => {
    if (!selectedFile) return;

    if (selectedFile.type !== "application/pdf") {
      setError("Please upload a PDF file.");
      return;
    }

    setFile(selectedFile);
    setError("");
    setMessage("");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      setUploading(true);

      const response = await api.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log(response.data);

      setMessage(
        `${response.data.filename} uploaded successfully (${response.data.chunks} chunks stored)`
      );
    } catch (err) {
      console.error(err);

      setError("Upload Failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-4">

      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFile(e.dataTransfer.files[0]);
        }}
        className={`cursor-pointer rounded-xl border-2 border-dashed p-6 text-center transition
        ${
          dragging
            ? "border-blue-500 bg-blue-500/10"
            : "border-slate-700 hover:border-blue-500"
        }`}
      >
        <Upload
          className="mx-auto mb-3 text-blue-400"
          size={40}
        />

        <p className="font-semibold">
          Drag & Drop PDF
        </p>

        <p className="mt-2 text-sm text-slate-400">
          or click to browse
        </p>

        <input
          ref={inputRef}
          type="file"
          hidden
          accept=".pdf"
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>

      {file && (
        <div className="flex items-center gap-3 rounded-lg bg-slate-800 p-3">
          <FileText className="text-green-400" size={28} />

          <div>
            <p className="font-medium">{file.name}</p>

            <p className="text-xs text-slate-400">
              {(file.size / 1024).toFixed(2)} KB
            </p>
          </div>
        </div>
      )}

      {uploading && (
        <div className="rounded-lg bg-blue-900/20 border border-blue-500 p-3">
          <p className="text-blue-400">
            ⏳ Uploading PDF...
          </p>
        </div>
      )}

      {message && (
        <div className="rounded-lg bg-green-900/20 border border-green-500 p-3">
          <p className="text-green-400">
            ✅ {message}
          </p>
        </div>
      )}

      {error && (
        <div className="rounded-lg bg-red-900/20 border border-red-500 p-3">
          <p className="text-red-400">
            ❌ {error}
          </p>
        </div>
      )}

    </div>
  );
}

export default UploadBox;