"use client";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import SingleCode from "@/components/single-code/SingleCode";
import UploadCode from "@/components/upload-code/UploadCode";
import GithubCode from "@/components/github-code/GithubCode";

const Page: React.FC = () => {
  return (
    <div className="container mx-auto p-10 h-screen justify-stretch">
      <Card className="p-5">
        <Tabs defaultValue="code" className="h-full">
          <TabsList className="mb-3">
            <TabsTrigger value="code">Code</TabsTrigger>
            <TabsTrigger value="upload">Upload</TabsTrigger>
            <TabsTrigger value="github">Github</TabsTrigger>
          </TabsList>

          <TabsContent asChild value="code">
            <SingleCode />
          </TabsContent>
          <TabsContent value="upload">
            <UploadCode />
          </TabsContent>
          <TabsContent value="github">
            <GithubCode />
          </TabsContent>
        </Tabs>
      </Card>
    </div>
  );
};

export default Page;
