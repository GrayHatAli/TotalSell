import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';

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
	})],
	server: {
		host: true,
		port: 5173,
		watch: {
			usePolling: true
		}
	}
});
