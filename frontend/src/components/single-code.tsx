import React, { useState } from "react";
import CodeEditor from "./ui/CodeEditor";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "./ui/label";
import { Button } from "./ui/button";

export const supported_languages = [
  "python",
  "cpp",
  "c",
  "java",
  "javascript",
  "typescript",
  "rust",
  "go",
  "kotlin",
  "swift",
];

const SingleCode = () => {
  const [value, setValue] = useState("");
  const [lang, setLang] = useState(supported_languages[0]);

  return (
    <div className="space-y-2">
      <fieldset className="flex items-center gap-10">
        <Label>Language</Label>

        <Select value={lang} onValueChange={setLang}>
          <SelectTrigger className="capitalize">
            <SelectValue placeholder="Language" />
          </SelectTrigger>
          <SelectContent>
            {supported_languages.map((language) => (
              <SelectItem
                className="capitalize"
                key={language}
                value={language}
              >
                {language}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </fieldset>

      <CodeEditor
        language={lang}
        onChange={(val) => {
          setValue(val);
        }}
        value={value}
      />

      <Button className="ml-auto" size={"lg"}>
        Submit
      </Button>
    </div>
  );
};

export default SingleCode;
