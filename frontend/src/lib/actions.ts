"use server";

import { getSingleGeneration } from "./api";
import { GetSingleGenerationResponse } from "./types";

export const getSingleGenerationAction = async (
  code: string
): Promise<GetSingleGenerationResponse> => {
  const data = await getSingleGeneration(code);
  return data;
};
