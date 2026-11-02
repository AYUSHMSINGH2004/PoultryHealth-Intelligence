import React from "react";
import * as ProgressPrimitive from "@radix-ui/react-slider";
import { cn } from "@/lib/utils";

const Progress = React.forwardRef(({ className, value, indicatorClassName, ...props }, ref) => (
  <div ref={ref} className={cn("relative h-4 w-full overflow-hidden rounded-full bg-white/10 backdrop-blur-sm", className)} {...props}>
    <div
      className={cn("h-full w-full flex-1 bg-gradient-to-r from-purple-500 to-blue-500 transition-all duration-500 ease-out", indicatorClassName)}
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
    />
  </div>
));
Progress.displayName = "Progress";

export { Progress };