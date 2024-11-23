"use client";
import Markdown from "react-markdown";
import CodeEditor from "../ui/CodeEditor";
import { OutputType } from "./types";
import Mermaid from "@/components/Mermaid";

type Props = {
  output: string;
  lang: string;
  type: OutputType;
};

const SingleCodeOutput = ({ lang, output, type }: Props) => {
  switch (type) {
    case "algo":
    case "guide":
      return (
        <Markdown className={"prose dark:prose-invert"}>{output}</Markdown>
      );
    case "code":
      return <CodeEditor language={lang} onChange={() => {}} value={output} />;
    case "diagram":
      return (
        <div className="bg-foreground px-10 rounded-md">
          <Mermaid chart={output} />
        </div>
      );
    default:
      throw new Error("Invalid output type");
  }
};

export default SingleCodeOutput;
