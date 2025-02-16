const defaultTheme = require('tailwindcss/defaultTheme');
const colors = require('tailwindcss/colors');

/** @type {import('tailwindcss').Config} */
export default {
    darkMode: ['class', '[data-mode="dark"]'],  // Updated dark mode setting
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
      "./components/**/*.{js,ts,jsx,tsx}" // Ensures shadcn components are styled
    ],
    theme: {
        extend: {
            fontFamily: {
				sans: [
					'Inter var',  
					'Poppins',  
					'Roboto',  
					'Nunito',  
					'Montserrat', 
					'Playfair Display',  
					'Lora',  
					...defaultTheme.fontFamily.sans
				],
				serif: [
					'Merriweather',  
					'PT Serif',  
					'Georgia', 
					...defaultTheme.fontFamily.serif
				],
				mono: [
					'Fira Code',  
					'JetBrains Mono',  
					'Source Code Pro', 
					...defaultTheme.fontFamily.mono
				],
			},
            spacing: {
				px: '1px',
				'0': '0rem',
				'0.5': '0.125rem', // 2px
				'1': '0.25rem', // 4px
				'1.5': '0.375rem', // 6px
				'2': '0.5rem', // 8px
				'2.5': '0.625rem', // 10px
				'3': '0.75rem', // 12px
				'3.5': '0.875rem', // 14px
				'4': '1rem', // 16px
				'5': '1.25rem', // 20px
				'6': '1.5rem', // 24px
				'7': '1.75rem', // 28px
				'8': '2rem', // 32px
				'9': '2.25rem', // 36px
				'10': '2.5rem', // 40px
				'12': '3rem', // 48px
				'14': '3.5rem', // 56px
				'16': '4rem', // 64px
				'20': '5rem', // 80px
				'24': '6rem', // 96px
				'28': '7rem', // 112px
				'32': '8rem', // 128px
				'36': '9rem', // 144px
				'40': '10rem', // 160px
				'44': '11rem', // 176px
				'48': '12rem', // 192px
				'52': '13rem', // 208px
				'56': '14rem', // 224px
				'60': '15rem', // 240px
				'64': '16rem', // 256px
				'72': '18rem', // 288px
				'80': '20rem', // 320px
				'96': '24rem', // 384px
				'128': '32rem', // 512px
				'144': '36rem', // 576px
				'160': '40rem', // 640px
				'192': '48rem', // 768px
				'256': '64rem', // 1024px
				'320': '80rem', // 1280px
			},
            borderRadius: {
				none: '0px',
				sm: '0.125rem', // 2px
				md: '0.375rem', // 6px
				lg: '0.5rem', // 8px
				xl: '0.75rem', // 12px
				'2xl': '1rem', // 16px
				'3xl': '1.5rem', // 24px
				'4xl': '2rem', // 32px
				'5xl': '2.5rem', // 40px
				'full': '9999px', // Fully rounded
			},
            colors: {
				transparent: 'transparent',
				current: 'currentColor',
			
				// Background & Foreground
				background: 'hsl(var(--background))',
				foreground: 'hsl(var(--foreground))',
			
				// Primary & Secondary Colors
				primary: {
					DEFAULT: 'hsl(var(--primary))',  // Main branding color
					foreground: 'hsl(var(--primary-foreground))',
					light: '#4F46E5', // Example: Indigo-600 (Vibrant)
					dark: '#312E81', // Example: Indigo-900 (Deep)
				},
				secondary: {
					DEFAULT: 'hsl(var(--secondary))',
					foreground: 'hsl(var(--secondary-foreground))',
					light: '#14B8A6', // Teal-500 (Vibrant)
					dark: '#0F766E', // Teal-800 (Deep)
				},
			
				// Accent Colors (Used for highlights, call-to-action, etc.)
				accent: {
					DEFAULT: 'hsl(var(--accent))',
					foreground: 'hsl(var(--accent-foreground))',
					light: '#EAB308', // Amber-500 (Bright & Noticeable)
					dark: '#B45309', // Amber-800 (Deep & Strong)
				},
			
				// Warning & Destructive (Errors & Alerts)
				warning: {
					DEFAULT: '#F59E0B', // Amber-400
					foreground: '#92400E', // Darker amber for contrast
				},
				destructive: {
					DEFAULT: 'hsl(var(--destructive))',
					foreground: 'hsl(var(--destructive-foreground))',
					light: '#EF4444', // Red-500 (Bright Warning)
					dark: '#991B1B', // Red-900 (Deep Error)
				},
			
				// Success & Confirmation
				success: {
					DEFAULT: '#22C55E', // Green-500 (Positive feedback)
					foreground: '#065F46', // Darker green for contrast
				},
			
				// Muted / Disabled
				muted: {
					DEFAULT: 'hsl(var(--muted))',
					foreground: 'hsl(var(--muted-foreground))',
					light: '#E5E7EB', // Neutral-200 (Subtle Grays)
					dark: '#6B7280', // Neutral-500 (Deeper Grays)
				},
			
				// Borders & Input Styles
				border: 'hsl(var(--border))',
				input: 'hsl(var(--input))',
				ring: 'hsl(var(--ring))',
			
				// Chart Colors (For Data Visualizations)
				chart: {
					'1': '#6366F1', // Indigo-500
					'2': '#10B981', // Emerald-500
					'3': '#F97316', // Orange-500
					'4': '#EAB308', // Amber-500
					'5': '#3B82F6', // Blue-500
				},
			
				// Dark Mode Colors
				dark: {
					background: '#111827', // Dark Blue Gray
					foreground: '#F9FAFB', // Near White
					primary: '#1E40AF', // Deep Blue
					secondary: '#047857', // Deep Teal
					accent: '#FACC15', // Bright Yellow
					destructive: '#B91C1C', // Deep Red
				},
			
				// Standard Colors (Material Design Palette)
				gray: colors.gray,
				slate: colors.slate,
				zinc: colors.zinc,
				neutral: colors.neutral,
				stone: colors.stone,
				red: colors.red,
				orange: colors.orange,
				amber: colors.amber,
				yellow: colors.yellow,
				lime: colors.lime,
				green: colors.green,
				emerald: colors.emerald,
				teal: colors.teal,
				cyan: colors.cyan,
				sky: colors.sky,
				blue: colors.blue,
				indigo: colors.indigo,
				violet: colors.violet,
				purple: colors.purple,
				fuchsia: colors.fuchsia,
				pink: colors.pink,
				rose: colors.rose,
			}
        }
    },
    plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography'), require("tailwindcss-animate")],
}
