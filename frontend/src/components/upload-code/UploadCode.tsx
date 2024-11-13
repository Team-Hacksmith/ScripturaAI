"use client";
import { cn, downloadFile } from "@/lib/utils";
import { ArrowDown, FileIcon, Trash2Icon } from "lucide-react";
import { useState } from "react";
import Dropzone from "react-dropzone";
import { Button } from "../ui/button";
import { getMultipleGenerationAction } from "@/lib/actions";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { supported_types } from "@/lib/config";
import { OutputType } from "../single-code/types";
import FakeProgress from "../ui/fake-progress";

const UploadCode = () => {
  const [files, setFiles] = useState<File[]>([]);
  const [type, setType] = useState<OutputType>("code");
  const [isPending, setIsPending] = useState(false);

  const addFiles = (newFiles: File[]) => {
    setFiles((files) => {
      const existingFilenames = new Set(files.map((file) => file.name));
      const uniqueNewFiles = newFiles.filter(
        (newFile) => !existingFilenames.has(newFile.name)
      );
      return [...files, ...uniqueNewFiles];
    });
  };

  const removeFile = (key: string) => {
    setFiles(files.filter((file) => file.name !== key));
  };

  return (
    <div className="relative flex flex-col items-center gap-5">
      <div className="flex flex-col lg:flex-row w-full gap-10">
        <Dropzone onDrop={(acceptedFiles) => addFiles(acceptedFiles)}>
          {({ getRootProps, getInputProps, isDragActive }) => (
            <section className="flex-1 text-center">
              <div
                className={cn(
                  "p-32 py-64 border border-dashed rounded-md flex flex-col gap-10 items-center justify-center",
                  { "border-foreground": isDragActive }
                )}
                {...getRootProps()}
              >
                <input {...getInputProps()} />

                <p>Drag n drop some files here, or click to select files</p>
              </div>
            </section>
          )}
        </Dropzone>
        <div className="flex flex-1 flex-col gap-2">
          {files.length === 0 && (
            <div className="w-full h-full flex items-center justify-center">
              No files selected
            </div>
          )}
          {files.map((file) => (
            <div
              className="hover:bg-destructive cursor-pointer rounded-lg w-full pr-5 flex items-center gap-2 group"
              onClick={() => removeFile(file.name)}
              key={file.name}
            >
              <div className="relative flex items-center justify-center w-9 h-9">
                <FileIcon className="absolute group-hover:opacity-0 transition-opacity" />
                <Trash2Icon className="absolute group-hover:opacity-100 opacity-0 transition-opacity" />
              </div>
              <span className="flex-1">{file.name}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="flex flex-col gap-3">
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
            const blob = await getMultipleGenerationAction(files, type);

            downloadFile(blob, "files.zip");

            setIsPending(false);
          }}
          variant={"outline"}
          isPending={isPending}
        >
          {isPending
            ? "Generating docs... This will take a while."
            : "Generate docs"}

          {!isPending && <ArrowDown />}
        </Button>
      </div>
      <FakeProgress className="bottom-full w-full" isPending={isPending} />
    </div>
  );
};

export default UploadCode;
