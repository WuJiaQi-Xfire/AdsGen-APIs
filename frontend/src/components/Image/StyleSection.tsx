import React from "react";
import { Square, CheckSquare } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { Input } from "@/components/UI/Input";
import { cn } from "@/lib/utils";
import { Style } from "@/lib/ImageGeneration";
import { Badge } from "@/components/UI/Badge";
import { Separator } from "@/components/UI/Separator";
import { StyleSettings } from "@/lib/ImagePresets";

interface StyleSectionProps {
  styleType: "lora" | "art";
  setStyleType: (type: "lora" | "art") => void;
  selectedStyles: string[];
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  selectMode: "single" | "multiple";
  setSelectMode: (mode: "single" | "multiple") => void;
  toggleStyleSelection: (styleId: string) => void;
  filteredStyles: Style[];
  selectAllStyles: () => void;
  clearStyleSelection: () => void;
  selectRandomStyle: () => void;
  fileInputRef: React.RefObject<HTMLInputElement>;
  setActiveStyleId: (id: string | null) => void;
  activeStyleId: string | null;
  addStyleSetting: (id: string, name: string) => void;
  removeStyleSetting: (id: string) => void;
  styleSettings: StyleSettings[];
  updateStyleSetting: (
    id: string,
    setting: keyof Omit<StyleSettings, "id" | "name">,
    value: number
  ) => void;
}

const StyleSection: React.FC<StyleSectionProps> = ({
  styleType,
  setStyleType,
  selectedStyles,
  searchQuery,
  setSearchQuery,
  selectMode,
  setSelectMode,
  toggleStyleSelection,
  filteredStyles,
  selectAllStyles,
  clearStyleSelection,
  selectRandomStyle,
  fileInputRef,
  setActiveStyleId,
  activeStyleId,
  addStyleSetting,
  removeStyleSetting,
  styleSettings,
  updateStyleSetting,
}) => {
  const handleStyleSelection = (style: Style, e: React.MouseEvent) => {
    e.stopPropagation();

    const isSelected = selectedStyles.includes(style.id);

    toggleStyleSelection(style.id);

    if (!isSelected) {
      addStyleSetting(style.id, style.name);
    } else {
      removeStyleSetting(style.id);

      if (activeStyleId === style.id) {
        setActiveStyleId(null);
      }
    }
  };

  const handleStyleClick = (style: Style) => {
    if (selectedStyles.includes(style.id)) {
      setActiveStyleId(style.id);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Button
            variant={styleType === "lora" ? "default" : "outline"}
            size="sm"
            onClick={() => setStyleType("lora")}
            className="h-8"
          >
            Lora Styles
          </Button>
          <Button
            variant={styleType === "art" ? "default" : "outline"}
            size="sm"
            onClick={() => setStyleType("art")}
            className="h-8"
          >
            Art Styles
          </Button>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <Input
            placeholder="Search styles..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="max-w-60"
          />
          <div className="flex items-center gap-1">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setSelectMode("single")}
              className={cn(
                "text-xs h-8",
                selectMode === "single" ? "bg-primary/10 border-primary/30" : ""
              )}
            >
              Single
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setSelectMode("multiple")}
              className={cn(
                "text-xs h-8",
                selectMode === "multiple"
                  ? "bg-primary/10 border-primary/30"
                  : ""
              )}
            >
              Multiple
            </Button>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-2">
          <Button
            variant="outline"
            size="sm"
            onClick={selectAllStyles}
            className="text-xs h-7"
          >
            Select All
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={clearStyleSelection}
            className="text-xs h-7"
          >
            Clear
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={selectRandomStyle}
            className="text-xs h-7 flex items-center gap-1"
          >
            Random
          </Button>
        </div>

        <Separator />

        <div className="flex flex-wrap gap-1.5 max-h-60 overflow-y-auto p-1">
          {filteredStyles.map((style) => (
            <Badge
              key={style.id}
              variant="outline"
              className={cn(
                "cursor-pointer py-1.5 px-3 transition-all duration-200 flex items-center gap-1.5",
                selectedStyles.includes(style.id)
                  ? "border-primary/15 bg-primary/40 hover:bg-primary/20"
                  : "hover:bg-accent",
                activeStyleId === style.id ? "ring-2 ring-primary" : ""
              )}
              onClick={() => handleStyleClick(style)}
            >
              <div
                className="flex items-center cursor-pointer p-1 rounded hover:bg-black/10 mr-1.5"
                onClick={(e) => handleStyleSelection(style, e)}
                title={
                  selectedStyles.includes(style.id)
                    ? "Click to deselect"
                    : "Click to select"
                }
              >
                {selectedStyles.includes(style.id) ? (
                  <CheckSquare className="h-5 w-5 text-primary flex-shrink-0" />
                ) : (
                  <Square className="h-5 w-5 text-muted-foreground flex-shrink-0" />
                )}
              </div>
              <span className="text-xs">{style.name}</span>
            </Badge>
          ))}
        </div>

        {selectedStyles.length > 0 && (
          <div className="mt-2 text-xs text-muted-foreground">
            <p>
              Click on the{" "}
              <Square className="h-4 w-4 inline-block mx-1 align-text-bottom" />{" "}
              checkbox to select/deselect styles
            </p>
            <p>Click on a selected style name to edit its settings</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StyleSection;
