import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0f",
        surface: "rgba(255,255,255,0.04)",
        border: "rgba(255,255,255,0.08)",
      },
      fontFamily: { sans: ["Inter", "system-ui", "sans-serif"] },
      animation: {
        gradient: "gradient 8s ease infinite",
        "fade-in": "fadeIn 0.5s ease",
      },
      keyframes: {
        gradient: {
          "0%, 100%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
        },
        fadeIn: { from: { opacity: "0", transform: "translateY(10px)" }, to: { opacity: "1", transform: "none" } },
      },
    },
  },
  plugins: [],
};
export default config;
