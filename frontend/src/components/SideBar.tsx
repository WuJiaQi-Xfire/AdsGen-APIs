import React, { useState } from "react";
import { 
  ImageIcon, 
  FileText,
  Menu, 
  X
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => {
    setCollapsed(!collapsed);
  };

  const menuItems = [
    {
      id: "prompt",
      name: "Prompt Generation",
      icon: <FileText className="h-5 w-5" />,
    },
    {
      id: "image",
      name: "Image Generation",
      icon: <ImageIcon className="h-5 w-5" />,
    },
  ];

  return (
    <div
      className={cn(
        "h-screen bg-sidebar border-r border-border fixed left-0 top-0 z-40 flex flex-col transition-all-300",
        collapsed ? "w-16" : "w-64"
      )}
    >
      <div className="flex items-center justify-between p-4 border-b border-border">
        {!collapsed && (
          <h1 className="text-xl font-semibold animate-fade-in">
            Ad Template
          </h1>
        )}
        <button
          onClick={toggleSidebar}
          className="sidebar-icon ml-auto"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <Menu className="h-5 w-5" /> : <X className="h-5 w-5" />}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto py-4 px-2">
        <nav className="space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={cn(
                "w-full flex items-center rounded-md p-2 transition-all-200",
                activeTab === item.id
                  ? "bg-primary text-primary-foreground"
                  : "hover:bg-accent hover:text-accent-foreground",
                collapsed ? "justify-center" : "justify-start"
              )}
            >
              <span className="flex-shrink-0">{item.icon}</span>
              {!collapsed && (
                <span className="ml-3 animate-fade-in">{item.name}</span>
              )}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;