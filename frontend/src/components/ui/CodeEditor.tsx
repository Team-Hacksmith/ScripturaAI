import React from "react";
import MonacoEditor from "@monaco-editor/react";

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  language: string;
  theme?: string;
}

const CodeEditor: React.FC<CodeEditorProps> = ({
  value,
  onChange,
  language,
  theme = "vs-dark",
}) => {
  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      onChange(value); // Ensure onChange gets the correct value
    }
  };

  return (
    <MonacoEditor
      height="640px" // Set the editor height
      language={language} // Set the language (e.g., javascript, python, etc.)
      value={value} // Set the initial code value
      onChange={handleEditorChange} // Handle code changes
      theme={theme} // Set theme (vs-dark, vs-light, etc.)
      className="rounded-md overflow-hidden"
      options={{
        selectOnLineNumbers: true, // Select line numbers
        automaticLayout: true, // Make layout adjustments automatically
        fontSize: 14, // Font size in editor
        minimap: { enabled: false }, // Disable minimap for simplicity
        scrollBeyondLastLine: false, // Disable scroll beyond last line
        wordWrap: "on", // Enable word wrapping
        padding: {
          top: 48,
          bottom: 48,
        },
      }}
    />
  );
};

export default CodeEditor;
