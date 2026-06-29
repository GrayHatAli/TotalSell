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
		extend: {}
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
