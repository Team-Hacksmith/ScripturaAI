export type OutputType = "markdown" | "mermaid" | "code";

export type SingleCodeOutput = {
  type: OutputType;
  content: string;
  lang?: string;
};
