<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { BrowserMultiFormatReader } from '@zxing/browser';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let videoEl: HTMLVideoElement;
	let reader: BrowserMultiFormatReader | null = null;
	let scanning = false;
	let error = '';

	onMount(async () => {
		try {
			reader = new BrowserMultiFormatReader();
			const devices = await BrowserMultiFormatReader.listVideoInputDevices();
			const deviceId = devices[0]?.deviceId;
			if (!deviceId) throw new Error('No camera found');
			await reader.decodeFromVideoDevice(deviceId, videoEl, (result) => {
				if (result) {
					dispatch('scanned', result.getText());
					stopScanning();
				}
			});
			scanning = true;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Camera error';
		}
	});

	function stopScanning() {
		if (reader) {
			reader.reset();
			reader = null;
		}
		scanning = false;
	}

	onDestroy(() => {
		stopScanning();
	});
</script>

<div class="space-y-2">
	{#if error}
		<div class="p-2 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded text-sm">
			{error} — use manual entry instead.
		</div>
	{/if}
	<video bind:this={videoEl} class="w-full rounded border" style="max-height: 240px;"></video>
	<div class="flex justify-end">
		<button class="btn btn-sm variant-soft-error" on:click={stopScanning} disabled={!scanning}>Cancel</button>
	</div>
</div>
