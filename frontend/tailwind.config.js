/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#10B981',
          dark: '#047857',
          light: '#D1FAE5',
          50: '#ECFDF5',
          100: '#D1FAE5',
          200: '#A7F3D0',
          300: '#6EE7B7',
          400: '#34D399',
          500: '#10B981',
          600: '#059669',
          700: '#047857',
          800: '#065F46',
          900: '#064E3B',
        },
        gold: {
          DEFAULT: '#F59E0B',
          light: '#FDE68A',
          dark: '#B45309',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          dark: '#172331',
        },
        night: {
          bg: '#0F1923',
          surface: '#172331',
          border: '#283747',
          text: '#F8FAFC',
          muted: '#9CA3AF',
        },
      },
      fontFamily: {
        arabic: ['Amiri', 'Noto Naskh Arabic', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'arabic-xs': ['1.5rem', { lineHeight: '2.5rem' }],
        'arabic-sm': ['1.75rem', { lineHeight: '3rem' }],
        'arabic-md': ['2rem', { lineHeight: '3.5rem' }],
        'arabic-lg': ['2.25rem', { lineHeight: '4rem' }],
        'arabic-xl': ['2.5rem', { lineHeight: '4.5rem' }],
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'slide-in': 'slideIn 0.3s ease-out',
        shimmer: 'shimmer 1.5s infinite',
        float: 'float 6s ease-in-out infinite',
        glow: 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        fadeIn: { from: { opacity: '0' }, to: { opacity: '1' } },
        slideUp: {
          from: { opacity: '0', transform: 'translateY(20px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          from: { opacity: '0', transform: 'translateX(-20px)' },
          to: { opacity: '1', transform: 'translateX(0)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          from: { boxShadow: '0 0 5px rgb(16 185 129 / 30%)' },
          to: { boxShadow: '0 0 20px rgb(16 185 129 / 70%)' },
        },
      },
      boxShadow: {
        glass: '0 8px 32px rgb(15 23 42 / 14%), inset 0 1px 0 rgb(255 255 255 / 10%)',
        card: '0 1px 3px rgb(15 23 42 / 8%), 0 8px 24px rgb(15 23 42 / 7%)',
        'card-hover': '0 8px 16px rgb(15 23 42 / 12%), 0 16px 38px rgb(15 23 42 / 9%)',
        gold: '0 4px 16px rgb(245 158 11 / 30%)',
        primary: '0 4px 16px rgb(16 185 129 / 35%)',
      },
      backgroundImage: {
        geometric:
          "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%2310B981' stroke-opacity='0.08' stroke-width='1'%3E%3Cpath d='M30 2l8 20 20 8-20 8-8 20-8-20-20-8 20-8z'/%3E%3C/g%3E%3C/svg%3E\")",
        'gradient-primary': 'linear-gradient(135deg, #10B981 0%, #047857 100%)',
        'gradient-gold': 'linear-gradient(135deg, #F59E0B 0%, #B45309 100%)',
        'gradient-dark': 'linear-gradient(135deg, #0F1923 0%, #172331 100%)',
        'shimmer-bg': 'linear-gradient(90deg, transparent 0%, rgb(255 255 255 / 8%) 50%, transparent 100%)',
      },
    },
  },
  plugins: [],
};
