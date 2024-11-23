"use client";
import { generateGithubWebsite } from "@/lib/api";
import { useState } from "react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { ArrowUpRight } from "lucide-react";
import FakeProgress from "../ui/fake-progress";

const GithubWebsite = () => {
  const [isPending, setIsPending] = useState(false);
  const [githubUrl, setGithubUrl] = useState("");
  const [liveUrl, setLiveUrl] = useState<null | string>(null);
  const [port, setPort] = useState("");
  const [title, setTitle] = useState("");

  return (
    <div className="relative w-full mx-auto flex flex-col items-center justify-center gap-2 min-h-[768px]">
      <div className="flex flex-col gap-5  py-10 max-w-sm">
        <fieldset>
          <Label>Enter the title for your website:</Label>
          <Input
            disabled={!!liveUrl}
            required
            autoFocus
            placeholder="Awesome Docs"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </fieldset>
        {/* <fieldset>
          <Label>Enter a port:</Label>
          <Input
            disabled={!!liveUrl}
            required
            autoFocus
            placeholder="8001"
            value={port}
            onChange={(e) => setPort(e.target.value)}
          />
        </fieldset> */}
        <fieldset>
          <Label>
            Enter a public github URL to clone and generate docs for:
          </Label>
          <Input
            disabled={!!liveUrl}
            required
            autoFocus
            placeholder="https://www.github.com/"
            value={githubUrl}
            onChange={(e) => setGithubUrl(e.target.value)}
          />
        </fieldset>
        {liveUrl ? (
          <div className="self-center flex gap-5">
            <a className="self-center" target="_blank" href={liveUrl}>
              <Button className="self-center">
                Visit Site <ArrowUpRight size={"16"} />
              </Button>
            </a>
            <Button
              onClick={() => {
                setGithubUrl("");
                setIsPending(false);
                setLiveUrl(null);
                setTitle("");
                setPort("");
              }}
              className="self-center"
              variant={"outline"}
            >
              Create New
            </Button>
          </div>
        ) : (
          <Button
            onClick={async () => {
              setIsPending(true);
              const { url } = await generateGithubWebsite(
                title,
                githubUrl,
                port
              );
              setLiveUrl(url);
              setIsPending(false);
            }}
            isPending={isPending}
            className="self-center"
          >
            Generate
          </Button>
        )}
      </div>
      <FakeProgress
        timeInterval={2000}
        className="bottom-full w-full"
        isPending={isPending}
      />
    </div>
  );
};

export default GithubWebsite;
