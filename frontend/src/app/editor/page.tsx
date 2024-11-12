"use client";

import CodeEditor from '@/components/ui/CodeEditor';
import { useState } from 'react';


const AddDoc: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [code, setCode] = useState<string>(''); // State to manage the code in the editor
  const [language, setLanguage] = useState<string>(''); // State to track the selected language

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = () => {
    if (file) {
      setLoading(true);
      // Simulate file upload with a timeout (replace with actual upload logic)
      setTimeout(() => {
        console.log("File uploaded:", file);
        setLoading(false); // Stop the spinner after upload
      }, 3000); // Simulate 3 seconds of upload time
    } else {
      alert("Please select a file before uploading.");
    }
  };

  const handleCodeChange = (newCode: string) => {
    setCode(newCode); // Update the state with the new code from the editor
  };

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(e.target.value); // Update the language based on user selection
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-md shadow-md">
      <h2 className="text-xl font-bold mb-4">Add Doc</h2>

      

      <label className="block text-sm font-medium mb-2">Select Language</label>
      <select
        className="w-full p-2 border border-gray-300 rounded-md mb-4"
        onChange={handleLanguageChange} // Handle language change
        value={language}
      >
        <option value="">Select Language</option>
        <option value="javascript">JavaScript</option>
        <option value="python">Python</option>
        <option value="java">Java</option>
        {/* Add more languages as needed */}
      </select>

      
      <label className="block text-sm font-medium mb-2">Code Editor</label>
      <CodeEditor
        value={code}
        onChange={handleCodeChange}
        language={language}
        theme="vs-dark" // You can set any theme here
      />

      <button
        onClick={handleSubmit}
        className="w-full bg-blue-500 text-white py-2 rounded-md font-bold hover:bg-blue-600 transition-colors flex items-center justify-center"
        disabled={loading} // Disable the button while loading
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
            <span>Submitting...</span>
          </div>
        ) : (
          "Submit"
        )}
      </button>
    </div>
  );
};

export default AddDoc;
