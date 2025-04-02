import React, { useState } from "react";
import { Input } from "@/components/UI/Input";
import { Separator } from "@/components/UI/Separator";
import { Slider } from "@/components/UI/Slider";
import { StyleSettings } from "@/lib/ImagePresets";
import { Check, ChevronDown, ChevronUp } from "lucide-react";
import { cn } from "@/lib/utils";
import { Style } from "@/lib/ImageGeneration";
import Select from "@/components/UI/Select";

interface ImageSettingsProps {
  aspectRatio: "1:1" | "16:9" | "9:16";
  handleAspectRatioChange: (aspectRatio: "1:1" | "16:9" | "9:16") => void;
  batchSize: number;
  styleStrength: number;
  setStyleStrength: (value: number) => void;
  setBatchSize: (value: number) => void;
  activeStyleId: string | null;
  activeStyleName?: string;
  selectedStyles: string[];
  styleSettings: StyleSettings[];
  updateStyleSetting: (
    id: string,
    setting: keyof Omit<StyleSettings, "id" | "name">,
    value: number | "1:1" | "16:9" | "9:16"
  ) => void;
  setActiveStyleId: (id: string | null) => void;
  filteredStyles: Style[];
}

const ImageSettings: React.FC<ImageSettingsProps> = ({
  styleStrength,
  setStyleStrength,
  aspectRatio,
  handleAspectRatioChange,
  batchSize,
  setBatchSize,
  activeStyleId,
  activeStyleName,
  selectedStyles,
  styleSettings,
  updateStyleSetting,
  setActiveStyleId,
  filteredStyles,
}) => {
  const [expandedStyleId, setExpandedStyleId] = useState<string | null>(null);

  const getStyleName = (styleId: string): string => {
    const style = filteredStyles.find((s) => s.id === styleId);
    return style?.name || styleId;
  };

  const toggleExpand = (styleId: string) => {
    if (expandedStyleId === styleId) {
      setExpandedStyleId(null);
    } else {
      setExpandedStyleId(styleId);
      setActiveStyleId(styleId);
    }
  };

  const getSettingsForStyle = (styleId: string) => {
    return (
      styleSettings.find((s) => s.id === styleId) || {
        styleStrength: 1,
        batchSize: 1,
        aspectRatio: "1:1",
      }
    );
  };

  return (
    <>
      <Separator />

      <div className="space-y-4">
        <h3 className="text-sm font-medium">Style Settings</h3>

        {selectedStyles.length > 0 ? (
          <div className="space-y-2">
            <p className="text-xs text-muted-foreground mb-2">
              Click on a style to customize its settings
            </p>

            <div className="space-y-2 max-h-[400px] overflow-y-auto">
              {selectedStyles.map((styleId) => {
                const settings = getSettingsForStyle(styleId);
                const isExpanded = expandedStyleId === styleId;
                const isActive = activeStyleId === styleId;

                return (
                  <div
                    key={styleId}
                    className={cn(
                      "border rounded-md overflow-hidden transition-all",
                      isActive && !isExpanded ? "ring-2 ring-primary" : ""
                    )}
                  >
                    <div
                      className={cn(
                        "flex justify-between items-center p-3 cursor-pointer",
                        isExpanded ? "bg-accent/20" : "hover:bg-accent/10"
                      )}
                      onClick={() => toggleExpand(styleId)}
                    >
                      <div className="flex items-center gap-2">
                        <Check
                          className={cn(
                            "h-4 w-4",
                            isActive
                              ? "text-primary"
                              : "text-muted-foreground/50"
                          )}
                        />
                        <span className="text-sm font-medium">
                          {getStyleName(styleId)}
                        </span>
                      </div>
                      {isExpanded ? (
                        <ChevronUp className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <ChevronDown className="h-4 w-4 text-muted-foreground" />
                      )}
                    </div>

                    {isExpanded && (
                      <div className="p-3 border-t bg-background space-y-3">
                        <div className="space-y-1">
                          <div className="flex justify-between">
                            <label className="text-xs text-muted-foreground">
                              Style Strength
                            </label>
                            <span className="text-xs">
                              {settings.styleStrength}
                            </span>
                          </div>
                          <Slider
                            value={[settings.styleStrength]}
                            min={0}
                            max={2}
                            step={0.1}
                            onValueChange={(values) =>
                              updateStyleSetting(
                                styleId,
                                "styleStrength",
                                values[0]
                              )
                            }
                          />
                        </div>

                        <div className="space-y-1">
                          <label className="text-xs text-muted-foreground">
                            Batch Size
                          </label>
                          <Input
                            type="number"
                            value={settings.batchSize}
                            onChange={(e) =>
                              updateStyleSetting(
                                styleId,
                                "batchSize",
                                parseInt(e.target.value, 10) || 1
                              )
                            }
                            min={1}
                            max={32}
                            className="text-xs"
                          />
                        </div>

                        <div className="space-y-1">
                          <label className="text-xs text-muted-foreground">
                            Aspect Ratio
                          </label>
                          <Select
                            value={settings.aspectRatio}
                            onValueChange={(value) =>
                              updateStyleSetting(
                                styleId,
                                "aspectRatio",
                                value as "1:1" | "16:9" | "9:16"
                              )
                            }
                            options={[
                              { value: "1:1", label: "1:1 (Square)" },
                              { value: "16:9", label: "16:9 (Landscape)" },
                              { value: "9:16", label: "9:16 (Portrait)" },
                            ]}
                            className="text-xs"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ) : (
          <div className="border rounded-md p-4 bg-accent/5 text-center">
            <p className="text-sm text-muted-foreground">
              Select styles from the left panel to customize their settings
            </p>
          </div>
        )}
      </div>
    </>
  );
};

export default ImageSettings;
