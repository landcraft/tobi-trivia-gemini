/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
      keyframes: {
        'bounce-in': {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.2)' },
        },
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '10%, 30%, 50%, 70%, 90%': { transform: 'translateX(-5px)' },
          '20%, 40%, 60%, 80%': { transform: 'translateX(5px)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      animation: {
        'bounce-in': 'bounce-in 0.5s ease-out',
        shake: 'shake 0.8s ease-in-out',
        'fade-in': 'fade-in 1s ease-out forwards',
      },
    },
  },
  plugins: [],
}