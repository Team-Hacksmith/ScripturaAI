"use server";

import { OutputType } from "@/components/single-code/types";
import { getSingleGeneration } from "./api";
import { GetSingleGenerationResponse } from "./types";

export const getSingleGenerationAction = async (
  code: string,
  type: OutputType
): Promise<GetSingleGenerationResponse> => {
  const data = await getSingleGeneration(code, type);
  return data;
};
