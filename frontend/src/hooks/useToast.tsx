import { createContext, useCallback, useContext, useState, ReactNode } from "react";

type Toast = { id: number; message: string; kind: "success" | "error" };
type ToastCtx = { toasts: Toast[]; push: (message: string, kind?: "success" | "error") => void };

const Ctx = createContext<ToastCtx | null>(null);

let nextId = 1;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const push = useCallback((message: string, kind: "success" | "error" = "success") => {
    const id = nextId++;
    setToasts((t) => [...t, { id, message, kind }]);
    setTimeout(() => {
      setToasts((t) => t.filter((x) => x.id !== id));
    }, 4000);
  }, []);

  return <Ctx.Provider value={{ toasts, push }}>{children}</Ctx.Provider>;
}

export function useToast(): ToastCtx {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useToast must be used inside ToastProvider");
  return ctx;
}