import { useState, useEffect } from 'react';
import { TabNavigation } from '@/components/TabNavigation';
import { toast } from "@/components/ToastManager";
import { Panel } from '@/components/Panel';
import { ModelSelector } from '@/components/ModelSelector';
import { FileUpload } from '@/components/FileUpload';
import { CustomSelect } from '@/components/CustomSelect';
import { TagInput } from '@/components/TagInput';
import { PrimaryButton } from '@/components/PrimaryButton';
import { Check, AlertCircle} from 'lucide-react';
import { ImageGenerationTab } from '@/components/ImageGenerationTab';
import { TABS, TEXT_MODEL_OPTIONS, VISUAL_GUIDANCE_OPTIONS, ITERATION_OPTIONS, LORA_OPTIONS } from '@/lib/config';

//Might need to disable Ollama first since no Vision 

const Index = () => {
  const [activeTab, setActiveTab] = useState('prompt');
  const [selectedModel, setSelectedModel] = useState('GPT');
  const [keywords, setKeywords] = useState<string[]>([]);
  const [visualGuidance, setVisualGuidance] = useState('lora');
  const [iteration, setIteration] = useState('all');
  const [loraOption, setLoraOption] = useState('');
  const [dataFile, setDataFile] = useState<File | null>(null);
  const [promptsFile, setPromptsFile] = useState<File | null>(null);
  const [ImageSetting, setImageSetting] = useState<any[]>([]);
  const [imageHeight, setImageHeight] = useState<number>(1024);
  const [imageWidth, setImageWidth] = useState<number>(1024);
  const [imagesPerPrompt, setImagesPerPrompt] = useState<number>(1);

  useEffect(() => {
    if (!promptsFile) {
      if (activeTab === 'image') {
        setActiveTab('prompt');
      }
    }else{
      setActiveTab('image');
    }
  }, [promptsFile, activeTab]);
 
  //For displaying of toast notficiation
  const handleGenerateClick = () => {
    if (keywords.length === 0) {
      toast.show({
        id: 'my-id',
        icon: <AlertCircle className="h-4 w-4" />,
        message: "Please add at least one keyword.",
        duration: 2000,
      });
      return;
    }

    toast.show({
        id: 'my-id',
        icon: <Check className="h-4 w-4" />,
        message: "Generation has started successfully!",
        duration: 2000,
      });
  };

  const handleTabChange = (tabId: string) => {
    {
    if (tabId === 'image' && !promptsFile) {
      toast.show({
        id:'my-id',
        icon: <AlertCircle className="h-4 w-4" />,
        message: 'Please upload a prompts file first.',
        duration: 2000,
      });
    }else if (tabId === 'prompt' && promptsFile) {
      toast.show({
        id:'my-id',
        icon: <AlertCircle className="h-4 w-4" />,
        message: 'Please deselect the prompts file.',
        duration: 2000,
      });
    }
    }
    setActiveTab(tabId);
  };


  //TODO: Requires proper file processing
  const handlePromptFileUpload = (file: File | null) => {
    setPromptsFile(file);
    //Placeholder
    if (file) {
      setImageSetting([{
        id: 1,
        keywords: 'Placeholder',
        template: 'Art Style: <lora:placeholder>'
      }]);
    } else {
      setImageSetting([]);
      if (activeTab === 'image') {
        setActiveTab('prompt');
      }
    }
  };

  const incrementImagesPerPrompt = () => {
    setImagesPerPrompt(prev => prev + 1);
  };

  const decrementImagesPerPrompt = () => {
    if (imagesPerPrompt > 1) {
      setImagesPerPrompt(prev => prev - 1);
    }
  };

  const handleImageUpload = (file: File | null) => {
    if (file) {
      
      {/*TODO: Add file handling instructions -> Send to backend, get the output keyword then display*/ }
      setTimeout(() => {
        const generatedKeywords = ['example1', 'example2', 'example3'];
        setKeywords([...keywords, ...generatedKeywords]);
      })
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center">
      <header className="w-full bg-gray-200 border-b border-gray-200 py-4 px-4 flex justify-center animate-fade-in">
        <div className="container max-w-6xl">
          <div className="flex items-center justify-center space-x-2">
            {/*Could add logo here if needed*/}
            <h1 className="text-2xl font-semibold">Ads Generator (V1.0)</h1>
          </div>
        </div>
      </header>

      <main className="container max-w-7xl w-full py-8 px-4 mt-8 animate-slide-up">
        <div className="flex">
          <div className="w-1/4 pr-8 space-y-6">
            <Panel title="AI Model">
              <ModelSelector 
                options={TEXT_MODEL_OPTIONS} 
                defaultSelected={selectedModel} 
                onChange={setSelectedModel} 
              />
            </Panel>
            {/*For future: add template/PSD/campaign panels*/}
            {/*TODO: Handle the 3 file uploads*/}

            <Panel title="Prompt list">
              <div className="space-y-4">
                <p className="text-sm text-gray-600 pt-2">Upload a prompt txt file</p>
                <FileUpload 
                  label="" 
                  onChange={setDataFile} 
                  accept=".txt" 
                />
              </div>
            </Panel>

            <Panel title="Keyword list">
              <div className="space-y-4">
                <p className="text-sm text-gray-600 pt-2">Upload a keyword list CSV file</p>
                <FileUpload 
                  label="" 
                  onChange={setDataFile} 
                  accept=".csv,.xlsx" 
                />
              </div>
            </Panel>
            
            <Panel title="Load previously generated prompts">
              <div className="space-y-4">
                <p className="text-sm text-gray-600 pt-2">Upload a generated prompts CSV file</p>
                <FileUpload 
                  label="" 
                  onChange={handlePromptFileUpload} 
                  accept=".csv" 
                />
              </div>
            </Panel>
          </div>

          <div className="w-3/4 bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
            <div className="p-8">
              <TabNavigation 
                tabs={TABS} 
                activeTab={activeTab} 
                onTabChange={handleTabChange}
              />
              {/*TODO: Add component for master prompt -> will do after adding the functionality to load prompts, not sure of the intended display now*/}
              <div className="py-8 space-y-8">
                {activeTab === 'prompt' ? (
                  <div className="space-y-6">
                    <div className="grid grid-cols-3 gap-6">
                      <CustomSelect
                        label="Visual Guidance"
                        options={VISUAL_GUIDANCE_OPTIONS}
                        value={visualGuidance}
                        onChange={setVisualGuidance}
                      />
                      
                      <CustomSelect
                        label="Iteration"
                        options={ITERATION_OPTIONS}
                        value={iteration}
                        onChange={setIteration}
                      />
                      
                      <CustomSelect
                        label="Select Loras"
                        options={LORA_OPTIONS}
                        value={loraOption}
                        onChange={setLoraOption}
                        placeholder="Choose an option"
                      />
                    </div>

                    <TagInput
                      label='Prompt added:'
                      description='Upload prompt list or click to generate'
                      placeholder='Type to generate prompt...'
                      tags={keywords}
                      onChange={setKeywords}
                      className='mb-4'
                    />
                    
                    <PrimaryButton onClick={handleGenerateClick}>
                      Generate prompt
                    </PrimaryButton>

                    <TagInput
                      label='Keywords added:'
                      description='Press Enter or comma to add'
                      placeholder='Type to add keywords...'
                      tags={keywords}
                      onChange={setKeywords}
                      className='mb-6'
                    />
                    
                    <div className="space-y-4">
                      <label className="text-sm font-medium text-gray-700">
                        Upload image to auto-generate keywords:
                      </label>
                      <FileUpload 
                        label="" 
                        onChange={handleImageUpload} 
                        //Supported image types by Vision
                        accept=".png, .jpeg, .jpg, .webp, .gif, image/png, image/jpeg, image/webp, image/gif" 
                      />
                    </div>

                    <div className="pt-4">
                      <p className="text-sm text-brand-red mb-4">
                        Enter at least one keyword and select one style in order to start the generation
                      </p>
                      
                      <PrimaryButton 
                        onClick={handleGenerateClick}
                        disabled={keywords.length === 0}
                      >
                        Start generation ({keywords.length})
                      </PrimaryButton>
                    </div>
                  </div>
                ) : (
                  <ImageGenerationTab 
                    ImageSetting={ImageSetting}
                    imageHeight={imageHeight}
                    imageWidth={imageWidth}
                    imagesPerPrompt={imagesPerPrompt}
                    setImageHeight={setImageHeight}
                    setImageWidth={setImageWidth}
                    incrementImagesPerPrompt={incrementImagesPerPrompt}
                    decrementImagesPerPrompt={decrementImagesPerPrompt}
                  />
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
