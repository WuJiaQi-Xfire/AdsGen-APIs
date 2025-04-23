import React from "react";
import { Download, Check } from "lucide-react";
import { Button } from "@/components/UI/PrimaryButton";
import { ScrollArea } from "@/components/UI/ScrollArea";

export interface GeneratedImage {
  url: string;
  filename?: string;
  selected: boolean;
}

interface ImageGalleryProps {
  images: GeneratedImage[];
  onSelectImage: (index: number) => void;
  onDownloadSelected: () => void;
  isLoading: boolean;
}

const ImageGallery: React.FC<ImageGalleryProps> = ({
  images,
  onSelectImage,
  onDownloadSelected,
  isLoading,
}) => {
  if (images.length === 0) {
    return null;
  }

  const selectedCount = images.filter((img) => img.selected).length;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Generated Images</h3>
        <span className="text-sm text-muted-foreground">
          {selectedCount} of {images.length} selected
        </span>
      </div>

      <Button
        onClick={onDownloadSelected}
        className="w-full bg-primary hover:bg-primary/90 text-white shadow-soft mb-4"
        size="default"
        disabled={selectedCount === 0 || isLoading}
      >
        <Download className="h-4 w-4 mr-2" />
        Download Selected ({selectedCount})
      </Button>

      <ScrollArea className="w-full h-[320px]">
        <div className="grid grid-cols-2 gap-3 pb-4 pr-4">
          {images.map((image, index) => (
            <div
              key={index}
              className={`
                relative rounded-md overflow-hidden border transition-all
                ${
                  image.selected
                    ? "ring-2 ring-primary border-primary"
                    : "border-border hover:border-muted-foreground"
                }
                cursor-pointer
              `}
              onClick={() => onSelectImage(index)}
            >
              <img
                src={`data:image/png;base64,${image.url}`}
                alt={`Generated image ${index + 1}`}
                className="w-full aspect-square object-cover"
              />

              {image.selected && (
                <div className="absolute top-2 right-2 bg-primary text-white rounded-full p-1">
                  <Check className="h-3 w-3" />
                </div>
              )}

              {image.filename !== undefined && (
                <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white p-2 text-xs truncate">
                  {image.filename}
                </div>
              )}
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
};

export default ImageGallery;
