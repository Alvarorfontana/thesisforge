import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ThesisForge — Generador académico glocal",
  description: "Generá módulos de tesis con rigor global y contexto argentino.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
