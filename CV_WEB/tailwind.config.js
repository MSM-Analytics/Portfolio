/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      screens: {
        'tablet': { 'min': '768px', 'max': '900px' },
      },
      fontFamily: {
        montserrat: ['Montserrat', 'sans-serif'],
        roboto: ['Roboto', 'sans-serif'],
        lato: ['Lato', 'sans-serif'],
        poppins: ['Poppins'],
        inter: ['Inter']
      },
      keyframes: {
        fadeUp: {
          '0%': {
            opacity: '0',
            transform: 'translateY(100px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        fadeDown: {
          '0%': {
            opacity: '0',
            transform: 'translateY(-100px)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0px)',
          },
        },
      },
      zoomIn: {
        '0%': {
          opacity: '0',
          transform: 'scale(0.5)',
        },
        '100%': {
          opacity: '1',
          transform: 'scale(1)',
        },
      },
      animation: {
        fadeUp: 'fadeUp 0.8s ease-out forwards',
        fadeDown: 'fadeDown 0.8s ease-out forwards',
        zoomIn: 'zoomIn 1.8s cubic-bezier(0.22, 1, 0.36, 1) forwards',
      },
    },
  },
  plugins: [],
}
