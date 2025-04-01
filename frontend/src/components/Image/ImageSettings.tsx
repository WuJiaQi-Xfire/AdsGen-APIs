import React from "react";
import { Input } from "@/components/UI/Input";
import { Separator } from "@/components/UI/Separator";
import { Slider } from "@/components/UI/Slider";

interface ImageSettingsProps {
  resolution: { width: number; height: number };
  handleResolutionChange: (
    dimension: "width" | "height",
    value: string
  ) => void;
  batchSize: number;
  styleStrength: number;
  setStyleStrength: (value: number) => void;
  setBatchSize: (value: number) => void;
}

const ImageSettings: React.FC<ImageSettingsProps> = ({
  styleStrength,
  setStyleStrength,
  resolution,
  handleResolutionChange,
  batchSize,
  setBatchSize,
}) => {
  return (
    <>
      <Separator />

      <div className="space-y-4">
        <h3 className="text-sm font-medium">Image Settings</h3>

        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-xs text-muted-foreground">Resolution</label>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">
                  Width
                </label>
                <Input
                  type="number"
                  value={resolution.width}
                  onChange={(e) =>
                    handleResolutionChange("width", e.target.value)
                  }
                  min={64}
                  max={2048}
                  step={64}
                  className="text-xs"
                />
              </div>
              <div>
                <label className="text-xs text-muted-foreground mb-1 block">
                  Height
                </label>
                <Input
                  type="number"
                  value={resolution.height}
                  onChange={(e) =>
                    handleResolutionChange("height", e.target.value)
                  }
                  min={64}
                  max={2048}
                  step={64}
                  className="text-xs"
                />
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex justify-between">
              <label className="text-xs text-muted-foreground">
                Style Strength
              </label>
              <span className="text-xs">{styleStrength}%</span>
            </div>
            <Slider
              value={[styleStrength]}
              min={0}
              max={2}
              step={0.1}
              onValueChange={(values) => setStyleStrength(values[0])}
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs text-muted-foreground mb-1 block">
              Batch Size
            </label>
            <Input
              type="number"
              value={batchSize}
              onChange={(e) => setBatchSize(parseInt(e.target.value, 10) || 1)}
              min={1}
              max={32}
              className="text-xs"
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default ImageSettings;
