import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import type { Plugin, ResolvedConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

// Custom plugin to override cssMinify after SvelteKit sets it
const overrideCssMinify: Plugin = {
	name: 'override-css-minify',
	enforce: 'post',
	configResolved(config: ResolvedConfig) {
		// Force esbuild for CSS minification to avoid lightningcss strictness
		// with Skeleton's ::file-selector-button:disabled pseudo-class
		config.build.cssMinify = 'esbuild';
		config.css.transformer = 'postcss';
	}
};

export default defineConfig({
	plugins: [sveltekit(), VitePWA({
		registerType: 'autoUpdate',
		workbox: {
			globPatterns: ['**/*.{js,css,html,ico,png,svg,woff,woff2}'],
			runtimeCaching: [
				{
					urlPattern: ({ request }) => request.destination === 'image',
					handler: 'CacheFirst',
					options: {
						cacheName: 'images',
						expiration: { maxEntries: 60, maxAgeSeconds: 30 * 24 * 60 * 60 }
					}
				}
			]
		},
		manifest: false
	}), overrideCssMinify],
	build: {
		// Skeleton UI generates CSS like `::file-selector-button:disabled` which
		// lightningcss rejects; esbuild's minifier is more lenient.
		// SvelteKit reads build.minify to set cssMinify
		minify: 'esbuild',
		cssMinify: 'esbuild'
	},
	css: {
		// Use postcss transformer instead of lightningcss to avoid strict
		// pseudo-class validation that breaks Skeleton's ::file-selector-button:disabled
		transformer: 'postcss'
	},
	server: {
		host: true,
		port: 5173,
		watch: {
			usePolling: true
		}
	}
});
