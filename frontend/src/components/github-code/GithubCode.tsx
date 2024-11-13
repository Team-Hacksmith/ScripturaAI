"use client";
import { getGenerationFromGithubAction } from "@/lib/actions";
import { downloadFile } from "@/lib/utils";
import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import FakeProgress from "../ui/fake-progress";

const GithubCode = () => {
  const [isPending, setIsPending] = useState(false);
  const [url, setUrl] = useState("");

  return (
    <div className="relative py-10 flex flex-col items-center justify-center gap-2 min-h-[768px]">
      <div className="flex max-w-lg mx-auto flex-col gap-2 w-full">
        <Label>Enter a public github URL to clone and generate docs for:</Label>
        <Input
          autoFocus
          placeholder="https://www.github.com/"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <Button
          onClick={async () => {
            setIsPending(true);
            const blob = await getGenerationFromGithubAction(url, "code");

            downloadFile(blob, "files.zip");

            setIsPending(false);
          }}
          isPending={isPending}
          className="self-center"
        >
          Generate
        </Button>
      </div>
      <FakeProgress className="bottom-full w-full" isPending={isPending} />
    </div>
  );
};

export default GithubCode;
