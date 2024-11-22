"use client";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getSingleGenerationAction } from "@/lib/actions";
import { supported_languages, supported_types } from "@/lib/config";
import { ArrowRight } from "lucide-react";
import { useState } from "react";
import { Button } from "../ui/button";
import CodeEditor from "../ui/CodeEditor";
import FakeProgress from "../ui/fake-progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../ui/tabs";
import SingleCodeOutput from "./SingleCodeOutput";
import { OutputType, SingleCodeOutput as SingleCodeOutputT } from "./types";

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
      <div className="flex flex-col xl:flex-row gap-5">
        <div className="relative xl:flex-1">
          <Select value={lang} onValueChange={setLang}>
            <SelectTrigger className="capitalize max-w-[160px] absolute z-10 bg-background px-3 right-1 top-1 opacity-70 hover:opacity-100 focus:opacity-100 focus-within:opacity-100 active:opacity-100 transition-opacity py-2 rounded flex items-center gap-10">
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
          <CodeEditor
            language={lang}
            onChange={(val) => {
              setValue(val);
            }}
            value={value}
          />
        </div>

        <div className="flex flex-col gap-2 items-center py-10">
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
              const data = await getSingleGenerationAction(value, type);
              createOutput({ type: data.type, content: data.content });
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
        <div className="xl:flex-1 relative">
          <FakeProgress isPending={isPending} timeInterval={1000} />
          {outputs.length > 0 ? (
            <Tabs className="relative" defaultValue={outputs[0].type + 0}>
              <TabsList className="absolute z-10 bottom-full mb-3">
                {outputs.map((op, i) => (
                  <TabsTrigger
                    value={op.type + i}
                    key={"trigger" + op.type + i}
                    className="capitalize"
                  >
                    {op.type} #{i + 1}
                  </TabsTrigger>
                ))}
              </TabsList>
              {outputs.map((op, i) => (
                <TabsContent
                  className="relative"
                  key={"output" + op.type + i}
                  value={op.type + i}
                >
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
