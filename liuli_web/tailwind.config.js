module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {},
    colors:{
      primary:'var(--theme-color)',
      textColor:'var(--default-text-color)'
    },
  },
  plugins: [require('@tailwindcss/line-clamp')],
}
