import React, { useState } from "react";
import { Upload, Link, X, Check } from "lucide-react";
import { Input } from "@/components/UI/Input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/UI/Tabs";

interface ReferenceImageProps {
  hasReferenceImage: boolean;
  fileName: string;
  imageUrl: string;
  setImageUrl: (url: string) => void;
  handleReferenceImageUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  clearReferenceImage: () => void;
}

const ReferenceImage: React.FC<ReferenceImageProps> = ({
  hasReferenceImage,
  fileName,
  imageUrl,
  setImageUrl,
  handleReferenceImageUpload,
  clearReferenceImage
}) => {
  const [activeTab, setActiveTab] = useState<string>("upload");

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium">Reference image</label>
      
      <Tabs 
        defaultValue="upload" 
        value={activeTab}
        onValueChange={(value) => {
          setActiveTab(value);
          if (value === "none") {
            clearReferenceImage();
          }
        }}
        className="w-full"
      >
        <TabsList className="grid grid-cols-3 w-full">
          <TabsTrigger value="upload" className="flex items-center gap-2">
            <Upload className="h-4 w-4" />
            <span>Upload</span>
          </TabsTrigger>
          <TabsTrigger value="url" className="flex items-center gap-2">
            <Link className="h-4 w-4" />
            <span>URL</span>
          </TabsTrigger>
          <TabsTrigger value="none" className="flex items-center gap-2">
            <X className="h-4 w-4" />
            <span>None</span>
          </TabsTrigger>
        </TabsList>
        
        <TabsContent value="upload">
          <label
            className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer hover:border-primary/50 hover:bg-accent transition-all duration-200 block ${
              hasReferenceImage && activeTab === "upload" ? "border-primary/50 bg-primary/5" : ""
            }`}
          >
            <input 
              type="file" 
              className="hidden" 
              //Current image types supported by Vision
              accept=".png, .jpeg, .jpg, .webp, .gif"
              onChange={handleReferenceImageUpload}
            />
            <div className="flex flex-col items-center justify-center py-4">
              <div className="bg-primary/10 rounded-full p-3 mb-2">
                {hasReferenceImage && activeTab === "upload" ? (
                  <Check className="h-6 w-6 text-primary" />
                ) : (
                  <Upload className="h-6 w-6 text-primary" />
                )}
              </div>
              <p className="text-sm font-medium">
                {hasReferenceImage && activeTab === "upload"
                  ? fileName
                  : "Click to upload image"}
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                JPG, PNG, WEBP (max. 5MB)
              </p>
            </div>
          </label>
        </TabsContent>
        
        <TabsContent value="url">
          <div className="space-y-4">
            <Input
              type="url"
              placeholder="Enter image URL"
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
              className="w-full"
            />
            {imageUrl && (
              <div className="text-sm text-center text-muted-foreground">
                URL provided: {imageUrl.length > 40 ? `${imageUrl.substring(0, 40)}...` : imageUrl}
              </div>
            )}
          </div>
        </TabsContent>
        
        <TabsContent value="none">
          <div className="border rounded-lg p-6 text-center">
            <div className="flex flex-col items-center justify-center py-4">
              <div className="bg-muted rounded-full p-3 mb-2">
                <X className="h-6 w-6 text-muted-foreground" />
              </div>
              <p className="text-sm text-muted-foreground">
                No reference image will be used
              </p>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ReferenceImage;