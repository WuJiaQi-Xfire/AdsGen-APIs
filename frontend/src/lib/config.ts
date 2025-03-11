export const TEXT_MODEL_OPTIONS = [
    { id: 'GPT', name: 'GPT' },
    { id: 'Ollama', name: 'Ollama' }
  ];
  
  export const VISUAL_GUIDANCE_OPTIONS = [
    { value: 'lora', label: 'Lora' },
    { value: 'art-style', label: 'Art-style' }
  ];
  
  export const ITERATION_OPTIONS = [
    { value: 'all', label: 'Use all selected loras per concept' },
    { value: 'individual', label: 'Use Individual loras' }
  ];
  //Placeholder, TODO: file handling
  export const LORA_OPTIONS = [
    { value: 'option1', label: 'Choose an option' },
    { value: 'option2', label: 'Placeholder' },
    { value: 'option3', label: 'Placeholder' }
  ];
  
  export const TABS = [
    { id: 'prompt', label: 'Prompt Generation' },
    { id: 'image', label: 'Image Generation' }
  ];
  