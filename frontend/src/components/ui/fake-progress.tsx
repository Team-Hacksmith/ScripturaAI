import { cn } from "@/lib/utils";
import * as ProgressPrimitive from "@radix-ui/react-progress";
import React, { useEffect, useState } from "react";
import { Progress } from "./progress";

type Props = {
  isPending: boolean;
  timeInterval?: number;
} & React.ComponentPropsWithoutRef<typeof ProgressPrimitive.Root>;

const FakeProgress = ({
  isPending,
  className,
  timeInterval = 500,
  ...props
}: Props) => {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isPending) {
      interval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 5, 95));
      }, timeInterval);
    } else {
      setProgress(0);
    }
    return () => clearInterval(interval);
  }, [isPending, timeInterval]);

  return (
    <Progress
      className={cn(
        "absolute z-10 transition-opacity",
        {
          "opacity-0": !isPending,
          "opacity-100": isPending,
        },
        className
      )}
      value={progress}
      {...props}
    />
  );
};

export default FakeProgress;
