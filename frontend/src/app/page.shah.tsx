"use client";

import { useState } from 'react';

const AddDoc: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (file) {
      setLoading(true);
      setTimeout(() => {
        console.log("File uploaded:", file);
        setLoading(false); 
      }, 3000); 
    } else {
      alert("Please select a file before uploading.");
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-md shadow-md ">
      <h2 className="text-xl font-bold mb-4">Add Doc</h2>

      <label className="block text-sm font-medium mb-2">Title</label>
      <input
        type="text"
        className="w-full p-2 border border-gray-300 rounded-md mb-4"
        placeholder="Enter title"
      />

      <label className="block text-sm font-medium mb-2">Select Language</label>
      <select className="w-full p-2 border border-gray-300 rounded-md mb-4">
        <option value="">Select Language</option>
        <option value="en">English</option>
        <option value="es">Spanish</option>
        <option value="fr">French</option>
        {/* Add more languages as needed */}
      </select>

      <label className="block text-sm font-medium mb-2">Drag Your File Here</label>
      <input
        type="file"
        onChange={handleFileChange}
        className="w-full p-4 border border-dashed border-gray-300 rounded-md mb-4 cursor-pointer"
      />

      <button
        onClick={handleUpload}
        className="w-full bg-blue-500 text-white py-2 rounded-md font-bold hover:bg-blue-600 transition-colors flex items-center justify-center"
        disabled={loading} 
      >
        {loading ? (
          <div className="flex items-center space-x-2">
            <svg
              className="animate-spin h-5 w-5 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
              ></path>
            </svg>
            <span>Uploading...</span>
          </div>
        ) : (
          "Upload"
        )}
      </button>
    </div>
  );
};

export default AddDoc;
