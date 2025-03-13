import React from "react";
import { Plus, X, ImagePlus } from "lucide-react";
import { Input } from "@/components/UI/Input";
import { Button } from "@/components/UI/PrimaryButton";
import { Badge } from "@/components/UI/Badge";

interface KeywordSectionProps {
  keyword: string;
  setKeyword: (keyword: string) => void;
  keywords: string[];
  handleAddKeyword: () => void;
  handleRemoveKeyword: (keyword: string) => void;
  handleKeywordImageUpload: () => void;
}

const KeywordSection: React.FC<KeywordSectionProps> = ({
  keyword,
  setKeyword,
  keywords,
  handleAddKeyword,
  handleRemoveKeyword,
  handleKeywordImageUpload,
}) => {
  return (
    <div className="space-y-4">
      <h3 className="font-medium">Keywords</h3>

      <div className="space-y-2">
        <div className="flex">
          <Input
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="Enter keywords..."
            className="flex-1 rounded-r-none focus-visible:ring-0 focus-visible:ring-offset-0"
          />
          <Button
            onClick={handleAddKeyword}
            variant="default"
            className="rounded-l-none"
          >
            <Plus className="h-4 w-4" />
          </Button>
        </div>

        <div className="flex flex-wrap gap-2 min-h-24 p-2 border rounded-md bg-background">
          {keywords.map((k) => (
            <Badge
              key={k}
              variant="secondary"
              className="flex items-center gap-1"
            >
              {k}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => handleRemoveKeyword(k)}
              />
            </Badge>
          ))}
        </div>

        <Button
          variant="outline"
          size="sm"
          className="w-full"
          onClick={handleKeywordImageUpload}
        >
          <ImagePlus className="h-4 w-4 mr-2" />
          Extract Keywords from Image
        </Button>
      </div>
    </div>
  );
};

export default KeywordSection;
