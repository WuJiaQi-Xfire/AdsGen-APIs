import { toast } from "@/components/UI/ToastManager";

export function showToast(message: string) {
  toast.show({
    id: "my-id",
    message,
    duration: 1500,
  });
}
