"use client";
import { getGenerationFromGithubAction } from "@/lib/actions";
import { supported_types } from "@/lib/config";
import { downloadFile } from "@/lib/utils";
import { useState } from "react";
import { OutputType } from "../single-code/types";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";

const GithubCode = () => {
  const [type, setType] = useState<OutputType>("code");
  const [isPending, setIsPending] = useState(false);
  const [url, setUrl] = useState("");

  return (
    <div className="max-w-lg mx-auto py-10 flex flex-col items-center justify-center gap-2 min-h-[768px]">
      <div className="flex flex-col gap-2 w-full">
        <Label>Enter a public github URL to clone and generate docs for:</Label>
        <Input
          autoFocus
          placeholder="https://www.github.com/"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <Select
          value={type}
          onValueChange={(val) => setType(val as OutputType)}
        >
          <SelectTrigger className="capitalize w-full">
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
            const blob = await getGenerationFromGithubAction(url, type);

            downloadFile(blob, "files.zip");

            setIsPending(false);
          }}
          isPending={isPending}
          className="self-center"
        >
          Generate
        </Button>
      </div>
    </div>
  );
};

export default GithubCode;
