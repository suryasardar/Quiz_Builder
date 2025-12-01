// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // <--- IMPORTANT: This tells Tailwind to scan all files in src
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}