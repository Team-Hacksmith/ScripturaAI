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
      onChange(value); 
    }
  };

  return (
    <MonacoEditor
      height="640px" 
      language={language} 
      value={value} 
      onChange={handleEditorChange} 
      theme={theme} 
      className="rounded-md overflow-hidden"
      options={{
        selectOnLineNumbers: true, 
        automaticLayout: true, 
        fontSize: 14, 
        minimap: { enabled: false }, 
        scrollBeyondLastLine: false,
        wordWrap: "on", 
        padding: {
          top: 48,
          bottom: 48,
        },
      }}
    />
  );
};

export default CodeEditor;
