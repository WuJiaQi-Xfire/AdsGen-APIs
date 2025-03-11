import { cn } from '@/lib/utils';

interface PrimaryButtonProps {
  onClick: () => void;
  children: React.ReactNode;
  className?: string;
}

export const PrimaryButton = ({
  onClick,
  children,
  className
}: PrimaryButtonProps) => (
  <button
    className={cn(
      'primary-button flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-blue text-white hover:bg-brand-blue-dark transition-colors',
      className
    )}
    onClick={onClick}
  >
    {children}
  </button>
);
