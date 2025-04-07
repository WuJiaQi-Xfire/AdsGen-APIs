import React, { useState, useRef, useEffect } from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

interface SelectProps {
  value: string;
  onValueChange: (value: string) => void;
  options: { value: string; label: string }[];
  placeholder?: string;
  className?: string;
}

export const Select: React.FC<SelectProps> = ({
  value,
  onValueChange,
  options,
  placeholder = "Select an option",
  className,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const selectRef = useRef<HTMLDivElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const selectedOption = options.find((option) => option.value === value);

  const handleClickOutside = (event: MouseEvent) => {
    if (
      selectRef.current &&
      !selectRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    if (isOpen && selectRef.current && dropdownRef.current) {
      const rect = selectRef.current.getBoundingClientRect();
      const dropdownHeight = Math.min(dropdownRef.current.scrollHeight, 240);

      const spaceBelow = window.innerHeight - rect.bottom;
      const spaceAbove = rect.top;

      const showBelow =
        spaceBelow >= dropdownHeight || spaceBelow >= spaceAbove;

      dropdownRef.current.style.width = `${rect.width}px`;

      if (showBelow) {
        dropdownRef.current.style.top = `${rect.bottom}px`;
        dropdownRef.current.style.left = `${rect.left}px`;
        dropdownRef.current.style.maxHeight = `${Math.min(
          spaceBelow - 10,
          240
        )}px`;
      } else {
        dropdownRef.current.style.bottom = `${window.innerHeight - rect.top}px`;
        dropdownRef.current.style.left = `${rect.left}px`;
        dropdownRef.current.style.maxHeight = `${Math.min(
          spaceAbove - 10,
          240
        )}px`;
      }
    }
  }, [isOpen]);

  return (
    <div ref={selectRef} className={cn("relative w-full", className)}>
      <div
        className="flex items-center justify-between w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background cursor-pointer"
        onClick={() => setIsOpen(!isOpen)}
      >
        <span className={cn(!selectedOption && "text-muted-foreground")}>
          {selectedOption ? selectedOption.label : placeholder}
        </span>
        <ChevronDown className="h-4 w-4 opacity-50" />
      </div>

      {isOpen && (
        <div
          ref={dropdownRef}
          className="fixed z-[999] rounded-md border border-input bg-background shadow-md overflow-auto"
          style={{ maxHeight: "240px" }}
        >
          {options.map((option) => (
            <div
              key={option.value}
              className={cn(
                "px-3 py-2 text-sm cursor-pointer hover:bg-accent hover:text-accent-foreground",
                option.value === value && "bg-accent/50 text-accent-foreground"
              )}
              onClick={() => {
                onValueChange(option.value);
                setIsOpen(false);
              }}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Select;
