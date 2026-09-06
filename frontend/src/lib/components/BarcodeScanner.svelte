<script lang="ts">
	import { onDestroy } from 'svelte';
	import { BrowserMultiFormatReader, type IScannerControls } from '@zxing/browser';
	import { createEventDispatcher } from 'svelte';
	import { t } from '$lib/i18n';

	const dispatch = createEventDispatcher();

	let videoEl: HTMLVideoElement;
	let reader: BrowserMultiFormatReader | null = null;
	let controls: IScannerControls | null = null;
	let scanning = false;
	let starting = false;
	let error = '';

	/**
	 * Scanning requires a user gesture: browsers are far more willing to show
	 * the camera permission prompt from a direct click than from an automatic
	 * onMount() call.
	 */
	async function startScanning() {
		error = '';
		starting = true;
		try {
			reader = new BrowserMultiFormatReader();

			// Best effort: pick a video input device. This list can legitimately
			// be EMPTY the very first time a site is visited, before the user has
			// granted camera permission (enumerateDevices() only lists non-default
			// devices once permission is granted). So we must NOT treat "empty
			// list" as "no camera". decodeFromVideoDevice() without an id falls
			// back to getUserMedia({ video: { facingMode: 'environment' } }),
			// which triggers the permission prompt and only errors with
			// NotFoundError when no camera actually exists.
			let deviceId: string | undefined;
			try {
				const devices = await BrowserMultiFormatReader.listVideoInputDevices();
				deviceId = devices[0]?.deviceId || undefined;
			} catch {
				deviceId = undefined;
			}

			controls = await reader.decodeFromVideoDevice(deviceId, videoEl, (result) => {
				if (result) {
					dispatch('scanned', result.getText());
					stopScanning();
				}
			});
			scanning = true;
		} catch (e) {
			if (e instanceof DOMException && e.name === 'NotAllowedError') {
				error = "Camera permission was denied. Please allow camera access in your browser and macOS privacy settings, then try again.";
			} else if (e instanceof DOMException && e.name === 'NotFoundError') {
				error = 'No camera found — use manual entry instead.';
			} else {
				error = e instanceof Error ? e.message : 'Could not start the camera.';
			}
		} finally {
			starting = false;
		}
	}

	function stopScanning() {
		try {
			controls?.stop();
		} catch {
			// ignore cleanup errors
		}
		controls = null;
		reader = null;
		scanning = false;
		starting = false;
	}

	onDestroy(() => {
		stopScanning();
	});
</script>

<div class="space-y-2">
	{#if error}
		<div class="p-2 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded text-sm">
			{error}
		</div>
	{/if}
	<video bind:this={videoEl} class="w-full rounded border" style="max-height: 240px;">
		<track kind="captions" />
	</video>
	<div class="flex items-center justify-between gap-2">
		<button class="btn btn-sm btn-primary" on:click={startScanning} disabled={scanning || starting}>
			{#if starting}<span class="loading-ring mr-2"></span>{/if}
			{t('barcode.start')}
		</button>
		<button class="btn btn-sm variant-soft-error" on:click={stopScanning} disabled={!scanning}>
			Cancel
		</button>
	</div>
</div>
