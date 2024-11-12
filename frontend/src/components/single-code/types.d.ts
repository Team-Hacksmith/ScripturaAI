export type OutputType = "guide" | "algo" | "diagram" | "code";

export type SingleCodeOutput = {
  type: OutputType;
  content: string;
  lang?: string;
};
