/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0f4ff",
          500: "#4f46e5",
          600: "#4338ca",
          900: "#1e1b4b",
        },
      },
    },
  },
  plugins: [],
};
