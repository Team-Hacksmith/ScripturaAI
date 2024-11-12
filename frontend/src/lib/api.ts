import { BASE_URL } from "./config";
import { GetSingleGenerationResponse } from "./types";

export const getSingleGeneration = async (
  code: string
): Promise<GetSingleGenerationResponse> => {
  const response = await fetch(`${BASE_URL}/single`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: code }),
  });
  const data = await response.json();
  return data;
};
