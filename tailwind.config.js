/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html', 
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'void': '#050505',
        'charcoal': '#121212',
        'blood': '#8a0303',
        'blood-light': '#b91c1c',
        'mist': '#e5e5e5',
        'bone': '#a3a3a3',
      },
      fontFamily: {
        'serif': ['Merriweather', 'Playfair Display', 'serif'],
        'sans': ['Inter', 'Lato', 'sans-serif'],
      },
    },
  },
  
  plugins: [
    require('@tailwindcss/typography'),
  ],
}