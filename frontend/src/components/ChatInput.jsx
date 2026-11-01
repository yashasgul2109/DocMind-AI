
import { Send, Paperclip, X, Image as ImageIcon } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import api from "../services/api";

function ChatInput({ onSend }) {
  const [question, setQuestion] = useState("");
  const [selectedImage, setSelectedImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);

  const fileInputRef = useRef(null);

  // Generate and clean up image preview
  useEffect(() => {
    if (!selectedImage) {
      setPreview(null);
      return;
    }

    const imageUrl = URL.createObjectURL(selectedImage);
    setPreview(imageUrl);

    return () => URL.revokeObjectURL(imageUrl);
  }, [selectedImage]);

  const handleImageSelect = (e) => {
    const file = e.target.files?.[0];

    if (!file) return;

    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp"
    ];

    if (!allowedTypes.includes(file.type)) {
      alert("Please select a JPG, PNG or WEBP image.");
      e.target.value = "";
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      alert("Image size cannot exceed 10 MB.");
      e.target.value = "";
      return;
    }

    setSelectedImage(file);
  };

  const removeImage = () => {
    setSelectedImage(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSend = async () => {
    if ((!question.trim() && !selectedImage) || uploading) return;

    try {
      setUploading(true);

      let imageData = null;

      // Upload image to FastAPI
      if (selectedImage) {
        const formData = new FormData();
        formData.append("file", selectedImage);

        const response = await api.post(
          "/image/upload",
          formData
        );

        imageData = response.data;
      }

      // Pass question and image information to parent
      onSend(question.trim(), imageData);

      setQuestion("");
      setSelectedImage(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

    } catch (error) {
      console.error("Image upload failed:", error);
      alert(
        error.response?.data?.detail ||
        "Unable to upload image. Please try again."
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="border-t border-slate-800 bg-slate-900 p-5">

      {/* Image Preview */}
      {preview && (
        <div className="mb-3 relative inline-block">
          <img
            src={preview}
            alt="Selected"
            className="h-28 w-28 rounded-xl object-cover border border-slate-700"
          />

          <button
            onClick={removeImage}
            className="absolute -right-2 -top-2 rounded-full bg-red-600 p-1 text-white hover:bg-red-700"
            title="Remove image"
          >
            <X size={14} />
          </button>
        </div>
      )}

      <div className="flex items-center gap-3 rounded-xl bg-slate-800 p-3">

        {/* Hidden Image Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          onChange={handleImageSelect}
          className="hidden"
        />

        {/* Attachment Button */}
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="rounded-lg p-2 text-slate-400 hover:bg-slate-700 hover:text-white"
          title="Attach image"
        >
          <Paperclip size={20} />
        </button>

        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Ask anything..."
          className="flex-1 bg-transparent outline-none text-white"
        />

        {/* Send Button */}
        <button
          onClick={handleSend}
          disabled={
            uploading ||
            (!question.trim() && !selectedImage)
          }
          className="rounded-lg bg-blue-600 p-3 text-white transition hover:bg-blue-700 disabled:opacity-50"
        >
          {uploading ? (
            <span className="text-xs">Uploading...</span>
          ) : (
            <Send size={18} />
          )}
        </button>

      </div>

      {selectedImage && (
        <p className="mt-2 text-xs text-slate-400">
          <ImageIcon size={12} className="inline mr-1" />
          {selectedImage.name}
        </p>
      )}

    </div>
  );
}

export default ChatInput;
