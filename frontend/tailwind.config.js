/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/App.js","./src/components/Recordings/index.jsx","./src/components/Recordings/Card.jsx"],
  theme: {
    extend: {},
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: ["light","pastel"],
  },
}

