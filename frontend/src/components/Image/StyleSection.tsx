import React from "react";
import { Plus, Check, Sparkles, Palette } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { Input } from "@/components/UI/Input";
import { cn } from "@/lib/utils";
import { Style } from "@/lib/ArtStyleList";

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
}) => {
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
            <Sparkles className="h-3 w-3" />
            Random
          </Button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 max-h-60 overflow-y-auto p-1">
          {filteredStyles.map((style) => (
            <Button
              key={style.id}
              variant="outline"
              size="sm"
              className={cn(
                "h-16 flex flex-col justify-center items-center gap-1 transition-all",
                selectedStyles.includes(style.id)
                  ? "border-primary bg-primary/10"
                  : "hover:border-primary/50"
              )}
              onClick={() => toggleStyleSelection(style.id)}
            >
              <Palette className="h-4 w-4" />
              <span className="text-xs line-clamp-1">{style.name}</span>
              {selectedStyles.includes(style.id) && (
                <Check className="h-3 w-3 absolute top-1 right-1 text-primary" />
              )}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StyleSection;
