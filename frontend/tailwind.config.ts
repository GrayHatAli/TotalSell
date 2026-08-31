import type { Config } from 'tailwindcss';
import { skeleton } from '@skeletonlabs/tw-plugin';
import forms from '@tailwindcss/forms';

export default {
	darkMode: 'class',
	content: [
		'./src/**/*.{html,js,svelte,ts}',
		'./node_modules/@skeletonlabs/skeleton/**/*.{html,js,svelte,ts}'
	],
	theme: {
		extend: {
			colors: {
				primary: '#334155',
				'primary-foreground': '#FFFFFF',
				secondary: '#475569',
				accent: '#059669',
				background: '#F8FAFC',
				foreground: '#0F172A',
				muted: '#F2F3F4',
				border: '#E6E8EA',
				destructive: '#DC2626',
				ring: '#334155'
			},
			spacing: {
				'xs': '4px',
				'sm': '8px',
				'md': '16px',
				'lg': '24px',
				'xl': '32px',
				'2xl': '48px',
				'3xl': '64px'
			},
			boxShadow: {
				'sm': '0 1px 2px rgba(0,0,0,0.05)',
				'md': '0 4px 6px rgba(0,0,0,0.1)',
				'lg': '0 10px 15px rgba(0,0,0,0.1)',
				'xl': '0 20px 25px rgba(0,0,0,0.15)'
			},
			fontFamily: {
				'sans': ['Fira Sans', 'ui-sans-serif', 'system-ui'],
				'mono': ['Fira Code', 'ui-monospace', 'SFMono-Regular']
			}
		}
	},
	plugins: [
		forms,
		skeleton({
			themes: {
				preset: [
					{
						name: 'skeleton',
						enhancements: true
					}
				]
			}
		})
	]
} satisfies Config;
