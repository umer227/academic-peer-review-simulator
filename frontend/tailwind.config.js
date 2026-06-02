/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#1f2933",
        paper: "#f7f4ef",
        oxford: "#243b53",
        thesis: "#52606d",
      },
    },
  },
  plugins: [],
};
