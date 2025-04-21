import React, { useState, useRef } from "react";
import { getPsdTemplates, generateTemplateMulti } from "@/lib/api";
import { Button } from "@/components/UI/PrimaryButton";
import { Upload } from "lucide-react";
import Select from "@/components/UI/Select"; // Use your custom Select
import ImageGallery from "@/components/Image/ImageGallery";

interface PsdTemplate {
  name: string;
  url: string;
}

const uploadIconClass =
  "mx-auto mb-2 text-primary group-hover:scale-105 transition-transform duration-150";

const TemplateGenerationTab: React.FC = () => {
  const [baseImages, setBaseImages] = useState<File[]>([]);
  const [psdFile, setPsdFile] = useState<File | null>(null);
  const [psdTemplates, setPsdTemplates] = useState<PsdTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<string>("");
  const [isLoadingTemplates, setIsLoadingTemplates] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedImages, setGeneratedImages] = useState<
    { url: string; filename?: string; selected: boolean }[]
  >([]);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const psdInputRef = useRef<HTMLInputElement>(null);

  React.useEffect(() => {
    if (psdTemplates.length === 0) {
      setIsLoadingTemplates(true);
      getPsdTemplates()
        .then((templates) => setPsdTemplates(templates))
        .finally(() => setIsLoadingTemplates(false));
    }
  }, []);

  const handleUploadImage = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setBaseImages(Array.from(e.target.files));
    }
  };

  const handleUploadPsd = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPsdFile(e.target.files[0]);
      setSelectedTemplate(""); // clear selection if uploading new psd
    }
  };

  // When a template is selected, clear any uploaded PSD file.
  const handleSelectTemplate = (tpl: string) => {
    setSelectedTemplate(tpl);
    setPsdFile(null);
  };

  const handleGenerate = async () => {
    if (baseImages.length === 0 || (!psdFile && !selectedTemplate)) return;
    setIsGenerating(true);
    setGeneratedImages([]);

    try {
      const images = await generateTemplateMulti({
        images: baseImages,
        psdFile,
        psdTemplateName: selectedTemplate,
      });
      if (images && images.length > 0) {
        setGeneratedImages(images.map((img) => ({ ...img, selected: false })));
      } else {
        alert("Failed to generate images.");
      }
    } catch {
      alert("Failed to generate template images.");
    } finally {
      setIsGenerating(false);
    }
  };

  const templateOptions = psdTemplates.map((tpl) => ({
    value: tpl.name,
    label: tpl.name,
  }));

  return (
    <div className="w-full max-w-4xl mx-auto p-6 animate-fade-in">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight mb-1">
          Template Image Generation
        </h1>
        <p className="text-muted-foreground">
          Upload a base image and either a PSD template or select from available
          templates to generate a layered visual.
        </p>
      </div>

      <div className="space-y-6">
        {/* Image Upload Card */}
        <div className="bg-white rounded-lg shadow-soft p-6 border">
          <h2 className="font-semibold text-lg mb-3">Base Image</h2>
          <div
            className="border-2 border-dashed border-input rounded-lg bg-accent/30 hover:bg-accent/40 transition cursor-pointer p-8 flex flex-col items-center group"
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
          >
            <Upload className={uploadIconClass} size={38} />
            <div className="font-medium text-base text-center mb-1">
              {baseImages.length > 0 ? (
                <>
                  <span className="text-primary">Images uploaded: </span>
                  <span className="text-muted-foreground">
                    {baseImages.map((img) => img.name).join(", ")}
                  </span>
                  <span className="ml-2 text-xs text-secondary/80">
                    (click to change)
                  </span>
                </>
              ) : (
                <>
                  Click to upload images <br />
                  <span className="text-xs text-muted-foreground font-normal">
                    JPG, PNG, WEBP, GIF (max. 20MB each, multiple allowed)
                  </span>
                </>
              )}
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              multiple
              className="hidden"
              onChange={handleUploadImage}
              tabIndex={-1}
            />
          </div>
        </div>

        {/* PSD Upload & Select Card */}
        <div className="bg-white rounded-lg shadow-soft p-6 border">
          <h2 className="font-semibold text-lg mb-3">PSD Template</h2>
          <div className="flex flex-col md:flex-row gap-6">
            {/* Upload PSD file */}
            <div className="flex-1 min-w-[220px]">
              <div
                className="border-2 border-dashed border-input rounded-lg bg-accent/30 hover:bg-accent/40 transition cursor-pointer p-8 flex flex-col items-center group"
                onClick={() => psdInputRef.current?.click()}
                role="button"
                tabIndex={0}
              >
                <Upload className={uploadIconClass} size={34} />
                <div className="font-medium text-base text-center mb-1">
                  {psdFile ? (
                    <>
                      <span className="text-primary">PNG uploaded: </span>
                      <span className="text-muted-foreground">
                        {psdFile.name}
                      </span>
                      <span className="ml-2 text-xs text-secondary/80">
                        (click to change)
                      </span>
                    </>
                  ) : (
                    <>
                      Click to upload PNG template file <br />
                      <span className="text-xs text-muted-foreground font-normal">
                        .PNG only (max. 20MB)
                      </span>
                    </>
                  )}
                </div>
                <input
                  ref={psdInputRef}
                  type="file"
                  accept=".png"
                  className="hidden"
                  onChange={handleUploadPsd}
                  tabIndex={-1}
                />
              </div>
            </div>

            <div className="hidden md:flex items-center px-2 text-secondary/60 font-bold select-none">
              OR
            </div>
            <div className="my-2 md:hidden flex items-center justify-center font-bold text-secondary/60 select-none">
              OR
            </div>

            <div className="flex-1 flex flex-col gap-2 min-w-[220px]">
              <label className="font-medium mb-1 ml-1 text-sm">
                Or select a PNG Template
              </label>
              <Select
                value={selectedTemplate}
                onValueChange={handleSelectTemplate}
                options={templateOptions}
                placeholder={
                  isLoadingTemplates
                    ? "Loading templates..."
                    : "Select PNG Template"
                }
                className="w-full"
              />
              <span className="text-xs text-muted-foreground mt-1">
                {isLoadingTemplates && "Fetching template list..."}
                {!isLoadingTemplates &&
                  psdTemplates.length === 0 &&
                  "No PNG templates found."}
              </span>
            </div>
          </div>
        </div>

        <div>
          <Button
            className="mt-2 w-full bg-primary hover:bg-primary/90 text-white font-semibold shadow-soft text-base py-3 rounded-lg transition"
            disabled={
              baseImages.length === 0 ||
              (!psdFile && !selectedTemplate) ||
              isGenerating
            }
            onClick={handleGenerate}
            size="lg"
          >
            {isGenerating ? (
              "Generating..."
            ) : (
              <>
                Generate Template
                <Upload className="ml-2 h-5 w-5" />
              </>
            )}
          </Button>
        </div>

        {generatedImages.length > 0 && (
          <div className="my-8 mx-auto bg-white rounded-lg shadow-soft p-6 border max-w-2xl text-center">
            <div className="mb-2 font-semibold text-lg">
              Generated Templates
            </div>
            <ImageGallery
              images={generatedImages}
              onSelectImage={(idx) => {
                setGeneratedImages((imgs) =>
                  imgs.map((img, i) =>
                    i === idx ? { ...img, selected: !img.selected } : img
                  )
                );
              }}
              onDownloadSelected={() => {
                generatedImages.forEach((img) => {
                  if (img.selected) {
                    const a = document.createElement("a");
                    a.href = img.url;
                    a.download = img.filename || "generated_template.png";
                    a.click();
                  }
                });
              }}
              isLoading={isGenerating}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default TemplateGenerationTab;
