//Utility classes for styling
import type { Config } from "tailwindcss";
import tailwindcssAnimate from "tailwindcss-animate";

const config: Config = {
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        Roboto: ["Roboto", "sans-serif"],
      },
      colors: {
        border: "hsl(215 16% 87%)",
        input: "hsl(215 16% 87%)",
        ring: "hsl(224 76% 48%)",
        background: "hsl(0 0% 100%)",
        foreground: "hsl(224 71% 4%)",

        primary: {
          DEFAULT: "hsl(262 80% 50%)",
          foreground: "hsl(0 0% 100%)",
        },

        secondary: {
          DEFAULT: "hsl(215 20% 95%)",
          foreground: "hsl(222 47% 11%)",
        },

        destructive: {
          DEFAULT: "hsl(0 84% 60%)",
          foreground: "hsl(0 0% 100%)",
        },

        muted: {
          DEFAULT: "hsl(215 20% 95%)",
          foreground: "hsl(215 16% 47%)",
        },

        accent: {
          DEFAULT: "hsl(215 20% 95%)",
          foreground: "hsl(222 47% 11%)",
        },

        popover: {
          DEFAULT: "hsl(0 0% 100%)",
          foreground: "hsl(224 71% 4%)",
        },

        card: {
          DEFAULT: "hsl(0 0% 100%)",
          foreground: "hsl(224 71% 4%)",
        },

        sidebar: {
          DEFAULT: "hsl(260 60% 98%)",
          foreground: "hsl(224 71% 4%)",
          primary: "hsl(262 80% 50%)",
          "primary-foreground": "hsl(0 0% 100%)",
          accent: "hsl(260 50% 94%)",
          "accent-foreground": "hsl(262 80% 50%)",
          border: "hsl(260 50% 90%)",
          ring: "hsl(262 80% 50%)",
        },
      },
      borderRadius: {
        lg: "1rem",
        md: "0.75rem",
        sm: "0.5rem",
      },
      keyframes: {
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "fade-out": {
          from: { opacity: "1" },
          to: { opacity: "0" },
        },
        "slide-in": {
          from: { transform: "translateX(-20px)", opacity: "0" },
          to: { transform: "translateX(0)", opacity: "1" },
        },
        "slide-out": {
          from: { transform: "translateX(0)", opacity: "1" },
          to: { transform: "translateX(20px)", opacity: "0" },
        },
      },
      pulse: {
        "0%, 100%": { opacity: "1" },
        "50%": { opacity: "0.7" },
      },

      animation: {
        "fade-in": "fade-in 0.4s ease-in-out",
        "fade-out": "fade-out 0.4s ease-out",
        "slide-in": "slide-in 0.4s ease-out",
        "slide-out": "slide-out 0.4s ease-out",
        pulse: "pulse 2.5s cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },

      boxShadow: {
        soft: "0 6px 24px -4px rgba(0, 0, 0, 0.1)",
        glow: "0 0 20px rgba(124, 58, 237, 0.25)",
      },

      backgroundImage: {
        "purple-gradient":
          "linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(124, 58, 237, 0.05) 100%)",
      },
    },
  },
  plugins: [tailwindcssAnimate],
};

export default config;
