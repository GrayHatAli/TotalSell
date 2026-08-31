<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { createEventDispatcher } from 'svelte';
	import type { Toast as ToastItem } from '$lib/stores/toast';

	export let id: string;
	export let message: string;
	export let title: string | undefined = undefined;
	export let type: ToastItem['type'] = 'default';
	export let duration: number = 3000;
	export let placement: 'top' | 'bottom' = 'top';

	const dispatch = createEventDispatcher<{ close: { id: string } }>();
	let timeout: ReturnType<typeof setTimeout>;

	onMount(() => {
		timeout = setTimeout(() => dispatch('close', { id }), duration);
	});

	onDestroy(() => {
		clearTimeout(timeout);
	});
</script>

<div
	class="relative w-56 max-w-xs p-4 mb-4 flex flex-col space-y-2 rounded-lg border shadow-lg
		{type === 'success' ? 'border-green-200 bg-green-50' : type === 'error' ? 'border-red-200 bg-red-50' : type === 'warning' ? 'border-yellow-200 bg-yellow-50' : type === 'info' ? 'border-blue-200 bg-blue-50' : 'border-gray-200 bg-gray-50'}
		dark:{type === 'success' ? 'border-green-700/30 bg-green-900/20' : type === 'error' ? 'border-red-700/30 bg-red-900/20' : type === 'warning' ? 'border-yellow-700/30 bg-yellow-900/20' : type === 'info' ? 'border-blue-700/30 bg-blue-900/20' : 'border-gray-600/30 bg-gray-800/20'}
		animate-in fade-in slide-in-{placement === 'top' ? 'down' : 'up'}
		animate-out fade-out fade-out-{placement === 'top' ? 'up' : 'down'}
	"
>
	<div class="flex items-start space-x-3">
		<div class="flex-shrink-0">
			{#if type === 'success'}
				<svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
					<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2c.293.293.771.293 1.064 0l3-3a1 1 0 00-1.414-1.414z" clip-rule="evenodd" />
				</svg>
			{:else if type === 'error'}
				<svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
					<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 001.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
				</svg>
			{:else if type === 'warning'}
				<svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
					<path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.529 0-2.492-1.646-1.742-2.98l5.58-9.92zM11 13a1 1 0 100-2 1 1 0 000 2zm-1-8a1 1 0 011-1h.01a1 1 0 110 2H11a1 1 0 01-1-1z" clip-rule="evenodd" />
				</svg>
			{:else if type === 'info'}
				<svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
					<path fill-rule="evenodd" d="M18 10A8 8 0 112 10a8 8 0 0116 0zm-8-4a1 1 0 100 2 1 1 0 000-2zm1 4a1 1 0 10-2 0v3a1 1 0 102 0v-3z" clip-rule="evenodd" />
				</svg>
			{:else}
				<svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
					<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2c.293.293.771.293 1.064 0l3-3a1 1 0 00-1.414-1.414z" clip-rule="evenodd" />
				</svg>
			{/if}
		</div>
		<div class="flex-1 min-w-0">
			{#if title}
				<h3 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{title}</h3>
			{/if}
			<p class="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">{message}</p>
		</div>
		<div class="flex-shrink-0 flex items-start">
			<button
				type="button"
				aria-label="Dismiss notification"
				on:click={() => dispatch('close', { id })}
				class="rounded-md p-1.5 hover:bg-gray-200 dark:hover:bg-gray-600"
			>
				<svg class="h-4 w-4 text-gray-400 hover:text-gray-500 dark:text-gray-300 dark:hover:text-gray-200" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
				</svg>
			</button>
		</div>
	</div>
</div>
