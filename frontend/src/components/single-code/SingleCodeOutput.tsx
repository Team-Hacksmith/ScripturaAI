import CodeEditor from "../ui/CodeEditor";
import { OutputType } from "./types";

type Props = {
  output: string;
  lang: string;
  type: OutputType;
};

const SingleCodeOutput = ({ lang, output, type }: Props) => {
  switch (type) {
    case "markdown":
      return null;
    case "code":
      return <CodeEditor language={lang} onChange={() => {}} value={output} />;
    case "mermaid":
      return null;
    default:
      throw new Error("Invalid output type");
  }
};

export default SingleCodeOutput;
