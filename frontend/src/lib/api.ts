import { OutputType } from "@/components/single-code/types";
import { BASE_URL } from "./config";
import { GetSingleGenerationResponse } from "./types";

export const getSingleGeneration = async (
  code: string,
  type: OutputType
): Promise<GetSingleGenerationResponse> => {
  const response = await fetch(`${BASE_URL}/single`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: code, type }),
  });
  const data = await response.json();
  return data;
};

export const getMultipleGeneration = async (
  files: File[],
  type: OutputType
): Promise<Blob> => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append("file", file);
  });
  formData.append("type", type);
  const response = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });
  const data = await response.blob();
  return data;
};
