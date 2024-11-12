"use client";
import Markdown from "react-markdown";
import CodeEditor from "../ui/CodeEditor";
import { OutputType } from "./types";

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
      return <p>{JSON.stringify(output, null, 2)}</p>;
    default:
      throw new Error("Invalid output type");
  }
};

export default SingleCodeOutput;
