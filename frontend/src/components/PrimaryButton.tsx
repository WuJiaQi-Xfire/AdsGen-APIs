import { cn } from '@/lib/utils';

interface PrimaryButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  disabled?: boolean;
  className?: string;
}

export const PrimaryButton = ({
  onClick,
  children,
  disabled,
  className
}: PrimaryButtonProps) => (
  <button
    className={cn(
      'primary-button flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-blue text-white hover:bg-brand-blue-dark transition-colors',
      disabled && 'opacity-50 cursor-not-allowed',
      className
    )}
    onClick={onClick}
    disabled={disabled}
  >
    {children}
  </button>
);
