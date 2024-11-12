"use client";
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
import { getSingleGenerationAction } from "@/lib/actions";
import { ArrowRight } from "lucide-react";

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
  const [output, setOutput] = useState("");
  const [isPending, setIsPending] = useState(false);
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

      <div className="flex flex-col xl:flex-row gap-5 xl:items-center">
        <div className="xl:flex-1">
          <CodeEditor
            language={lang}
            onChange={(val) => {
              setValue(val);
            }}
            value={value}
          />
        </div>

        <Button
          onClick={async () => {
            setIsPending(true);
            const data = await getSingleGenerationAction(value);
            setOutput(data.content);
            setIsPending(false);
          }}
          className="ml-auto"
          variant={"outline"}
          size={"icon"}
          isPending={isPending}
        >
          <ArrowRight />
        </Button>
        <div className="xl:flex-1">
          <CodeEditor language={lang} onChange={() => {}} value={output} />
        </div>
      </div>
    </div>
  );
};

export default SingleCode;
