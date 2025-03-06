
import { cn } from '@/lib/utils';

interface TabNavigationProps {
  tabs: { id: string; label: string }[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
}

export const TabNavigation = ({ 
  tabs, 
  activeTab, 
  onTabChange 
}: TabNavigationProps) => {
  return (
    <div className="border-b border-gray-200">
      <div className="flex space-x-8">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={cn(
              "py-3 px-1 text-sm font-medium border-b-2 transition-all duration-200 relative",
              activeTab === tab.id 
                ? "text-brand-blue border-brand-blue" 
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  );
};
