import React, { useState, useEffect } from "react";
import Sidebar from "@/components/SideBar";
import PromptGeneration from "@/components/PromptGenerationTab";
import ImageGeneration from "@/components/ImageGenerationTab";

const Index: React.FC = () => {
  const [activeTab, setActiveTab] = useState("prompt");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/backend")
      .then((response) => response.json())
      .then((data) => console.log(data))
      .catch((error) => console.error("Error:", error));
  }, []);

  return (
    <div className="min-h-screen flex bg-purple-gradient">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <div className="flex-1 ml-64 transition-all-300">
        <main className="min-h-screen py-6 px-2">
          {activeTab === "prompt" && <PromptGeneration />}
          {activeTab === "image" && <ImageGeneration />}
        </main>
      </div>
    </div>
  );
};

export default Index;
