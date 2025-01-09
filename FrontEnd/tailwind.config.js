/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"], // Enable manual dark mode
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./src/**/*.{js,ts,jsx,tsx}" 
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        primary: {
          DEFAULT: "var(--primary)",
          hover: "var(--primary-hover)",
          foreground: "var(--primary-foreground)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          hover: "var(--secondary-hover)",
          foreground: "var(--secondary-foreground)",
        },
        destructive: {  
          DEFAULT: "#f44336", 
          hover: "#e53935",   
          foreground: "#ffffff",
        },
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
        modal: {
          DEFAULT: "var(--modal-background)",
          foreground: "var(--modal-foreground)",
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
