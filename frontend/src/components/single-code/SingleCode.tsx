"use client";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getSingleGenerationAction } from "@/lib/actions";
import { ArrowRight } from "lucide-react";
import { useState } from "react";
import { Button } from "../ui/button";
import CodeEditor from "../ui/CodeEditor";
import { Label } from "../ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import SingleCodeOutput from "./SingleCodeOutput";
import { OutputType, SingleCodeOutput as SingleCodeOutputT } from "./types";

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

export const supported_types = ["code", "markdown", "mermaid"];

const SingleCode = () => {
  const [value, setValue] = useState("");
  const [type, setType] = useState<OutputType>("code");

  const [outputs, setOutputs] = useState<SingleCodeOutputT[]>([]);
  const [isPending, setIsPending] = useState(false);
  const [lang, setLang] = useState(supported_languages[0]);

  const createOutput = (output: SingleCodeOutputT) => {
    setOutputs((op) => [...op, output]);
  };

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

        <div className="flex flex-col gap-2 items-center justify-center">
          <Select
            value={type}
            onValueChange={(val) => setType(val as OutputType)}
          >
            <SelectTrigger className="capitalize w-[120px]">
              <SelectValue placeholder="Type" />
            </SelectTrigger>
            <SelectContent>
              {supported_types.map((type) => (
                <SelectItem className="capitalize" key={type} value={type}>
                  {type}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Button
            onClick={async () => {
              setIsPending(true);
              const data = await getSingleGenerationAction(value);
              createOutput({ type: "code", content: data.content });
              setIsPending(false);
            }}
            className=""
            variant={"outline"}
            size={"icon"}
            isPending={isPending}
          >
            <ArrowRight />
          </Button>
        </div>
        <div className="xl:flex-1">
          {outputs.length > 0 ? (
            <Tabs defaultValue={outputs[0].type + 0}>
              <TabsList>
                {outputs.map((op, i) => (
                  <TabsTrigger
                    value={op.type + i}
                    key={"trigger" + op.type + i}
                    className="capitalize"
                  >
                    {op.type}
                  </TabsTrigger>
                ))}
              </TabsList>
              {outputs.map((op, i) => (
                <TabsContent key={"output" + op.type + i} value={op.type + i}>
                  {/* {op.content} */}
                  <SingleCodeOutput
                    lang={lang}
                    output={op.content}
                    type={op.type}
                  />
                </TabsContent>
              ))}
            </Tabs>
          ) : (
            <SingleCodeOutput lang={lang} output="" type="code" />
          )}
        </div>
      </div>
    </div>
  );
};

export default SingleCode;
