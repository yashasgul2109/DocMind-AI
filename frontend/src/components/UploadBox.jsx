import { Upload, FileText } from "lucide-react";
import { useRef, useState } from "react";
import api from "../services/api";

function UploadBox() {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);

const [uploading, setUploading] = useState(false);

const handleFile = async (selectedFile) => {
  if (!selectedFile) return;

  if (selectedFile.type !== "application/pdf") {
    alert("Please upload a PDF");
    return;
  }

  setFile(selectedFile);

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
    alert("PDF Uploaded Successfully!");
  } catch (err) {
    console.error(err);
    alert("Upload Failed");
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
          <FileText className="text-green-400" />
          <div>
            <p>{file.name}</p>
            <p className="text-xs text-slate-400">
              {(file.size / 1024).toFixed(1)} KB
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default UploadBox;