//Harded coded to show style selection, ideally we should have 1/2 styles for user to choose as well
export interface Style {
    id: string;
    name: string;
  }
  
  export const loraStyles: Style[] = [
    { id: "lora-cyberpunk anime", name: "Cyberpunk anime" },
    { id: "lora-gta style", name: "GTA Style" },
  ];
  
  export const artStyles: Style[] = [
    { id: "art-cartoon", name: "Cartoon Stylized Pixel Art Game Concept" },
    { id: "art-semi realistic", name: "Semi-Realistic Pixel Art Game Concept" },

  ];
  
  export const getStyles = (styleType: "lora" | "art", searchQuery: string) => {
    const currentStyles = styleType === "lora" ? loraStyles : artStyles;
    
    const filteredStyles = searchQuery 
      ? currentStyles.filter(style => 
          style.name.toLowerCase().includes(searchQuery.toLowerCase())
        )
      : currentStyles;
  
    return { filteredStyles, currentStyles };
  };