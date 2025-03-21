import React from "react";
import { Plus, X, Upload, Link, Loader } from "lucide-react";
import { Input } from "@/components/UI/Input";
import { Button } from "@/components/UI/PrimaryButton";
import { Badge } from "@/components/UI/Badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/UI/Tabs";

interface KeywordSectionProps {
  keyword: string;
  setKeyword: (keyword: string) => void;
  keywords: string[];
  isLoadingKeywords: boolean;
  handleAddKeyword: () => void;
  handleRemoveKeyword: (keyword: string) => void;
  handleKeywordImageUpload: (file?: File, imageUrl?: string) => void;
}

const KeywordSection: React.FC<KeywordSectionProps> = ({
  keyword,
  setKeyword,
  keywords,
  handleAddKeyword,
  isLoadingKeywords,
  handleRemoveKeyword,
  handleKeywordImageUpload,
}) => {
  const [keywordImageUrl, setKeywordImageUrl] = React.useState("");
  const [keywordTab, setKeywordTab] = React.useState("text");
  const keywordFileRef = React.useRef<HTMLInputElement>(null);

  const handleKeywordFileClick = () => {
    if (keywordFileRef.current && !isLoadingKeywords) {
      keywordFileRef.current.click();
    }
  };

  const handleFileSelection = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      handleKeywordImageUpload(file);
      if (keywordFileRef.current) {
        keywordFileRef.current.value = "";
      }
    }
  };

  const handleKeywordImageUrl = () => {
    if (keywordImageUrl.trim()) {
      handleKeywordImageUpload(undefined, keywordImageUrl);
      setKeywordImageUrl("");
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="font-medium text-lg">Keywords</h3>

      <div className="space-y-3">
        <Tabs
          value={keywordTab}
          onValueChange={setKeywordTab}
          className="w-full"
        >
          <TabsList className="grid grid-cols-3 mb-2 w-full bg-secondary">
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
                disabled={isLoadingKeywords}
              />
              <Button
                onClick={handleAddKeyword}
                variant="default"
                className="rounded-l-none"
                disabled={isLoadingKeywords}
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="file">
            <div
              className={`border-2 border-dashed rounded-md p-4 text-center ${
                isLoadingKeywords
                  ? "cursor-not-allowed opacity-70"
                  : "cursor-pointer hover:border-primary/50 hover:bg-accent/50"
              } transition-all`}
              onClick={!isLoadingKeywords ? handleKeywordFileClick : undefined}
            >
              <div className="flex flex-col items-center justify-center py-2">
                <div className="bg-primary/10 rounded-full p-2 mb-1">
                  {isLoadingKeywords ? (
                    <Loader className="h-4 w-4 text-primary animate-spin" />
                  ) : (
                    <Upload className="h-4 w-4 text-primary" />
                  )}
                </div>
                <p className="text-sm font-medium">
                  {isLoadingKeywords
                    ? "Extracting keywords..."
                    : "Upload image for keywords"}
                </p>
                {!isLoadingKeywords && (
                  <p className="text-xs text-muted-foreground mt-1">
                    JPG, JPEG, PNG, WEBP, GIF (max. 20MB)
                  </p>
                )}
              </div>
              <input
                type="file"
                ref={keywordFileRef}
                className="hidden"
                accept=".png, .jpeg, .jpg, .webp, .gif"
                onChange={handleFileSelection}
                disabled={isLoadingKeywords}
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
                disabled={isLoadingKeywords}
              />
              <Button
                onClick={handleKeywordImageUrl}
                variant="default"
                className="rounded-l-none"
                disabled={!keywordImageUrl.trim() || isLoadingKeywords}
              >
                {isLoadingKeywords ? (
                  <Loader className="h-4 w-4 animate-spin" />
                ) : (
                  <Link className="h-4 w-4" />
                )}
              </Button>
            </div>
          </TabsContent>
        </Tabs>

        <div className="flex flex-wrap gap-2 min-h-28 p-3 border rounded-md bg-background overflow-y-auto max-h-60">
          {isLoadingKeywords && keywords.length === 0 ? (
            <div className="w-full flex items-center justify-center py-7">
              <Loader className="h-5 w-5 text-primary animate-spin mr-2" />
              <p className="text-sm text-muted-foreground">
                Extracting keywords...
              </p>
            </div>
          ) : keywords.length === 0 ? (
            <p className="text-sm text-muted-foreground w-full text-center py-7">
              No keywords added yet.
            </p>
          ) : (
            keywords.map((k) => (
              <Badge
                key={k}
                variant="secondary"
                className="flex items-center gap-1 py-1.5 px-3"
              >
                {k}
                <X
                  className="h-3 w-3 cursor-pointer ml-1"
                  onClick={() => handleRemoveKeyword(k)}
                />
              </Badge>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default KeywordSection;
