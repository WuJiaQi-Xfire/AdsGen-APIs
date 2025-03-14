import React from "react";
import { Plus, X, ImagePlus, Upload, Link } from "lucide-react";
import { Input } from "@/components/UI/Input";
import { Button } from "@/components/UI/PrimaryButton";
import { Badge } from "@/components/UI/Badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/UI/Tabs";

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
  const [keywordImageUrl, setKeywordImageUrl] = React.useState("");
  const [keywordTab, setKeywordTab] = React.useState("text");
  const keywordFileRef = React.useRef<HTMLInputElement>(null);

  const handleKeywordFileClick = () => {
    if (keywordFileRef.current) {
      keywordFileRef.current.click();
    }
  };

  const handleKeywordImageUrl = () => {
    if (keywordImageUrl.trim()) {
      handleKeywordImageUpload();
      setKeywordImageUrl("");
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="font-medium">Keywords</h3>

      <div className="space-y-2">
        <Tabs
          value={keywordTab}
          onValueChange={setKeywordTab}
          className="w-full"
        >
          <TabsList className="grid grid-cols-3 mb-2">
            <TabsTrigger value="text" className="text-xs">
              Text Input
            </TabsTrigger>
            <TabsTrigger value="file" className="text-xs">
              Upload Image
            </TabsTrigger>
            <TabsTrigger value="url" className="text-xs">
              Image URL
            </TabsTrigger>
          </TabsList>

          <TabsContent value="text" className="space-y-2">
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
          </TabsContent>

          <TabsContent value="file">
            <div
              className="border-2 border-dashed rounded-md p-4 text-center cursor-pointer hover:border-primary/50 hover:bg-accent/50 transition-all"
              onClick={handleKeywordFileClick}
            >
              <div className="flex flex-col items-center justify-center py-2">
                <div className="bg-primary/10 rounded-full p-2 mb-1">
                  <Upload className="h-4 w-4 text-primary" />
                </div>
                <p className="text-sm font-medium">Upload image for keywords</p>
                <p className="text-xs text-muted-foreground mt-1">
                  JPG, JPEG, PNG, WEBP, GIF (max. 20MB)
                </p>
              </div>
              <input
                type="file"
                ref={keywordFileRef}
                className="hidden"
                accept=".png, .jpeg, .jpg, .webp, .gif"
                onChange={() => handleKeywordImageUpload()}
              />
            </div>
          </TabsContent>

          <TabsContent value="url" className="space-y-2">
            <div className="flex">
              <Input
                value={keywordImageUrl}
                onChange={(e) => setKeywordImageUrl(e.target.value)}
                placeholder="Enter image URL..."
                className="flex-1 rounded-r-none focus-visible:ring-0 focus-visible:ring-offset-0"
              />
              <Button
                onClick={handleKeywordImageUrl}
                variant="default"
                className="rounded-l-none"
                disabled={!keywordImageUrl.trim()}
              >
                <Link className="h-4 w-4" />
              </Button>
            </div>
          </TabsContent>
        </Tabs>

        <div className="flex flex-wrap gap-2 min-h-24 p-2 border rounded-md bg-background overflow-y-auto max-h-48">
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
      </div>
    </div>
  );
};

export default KeywordSection;
