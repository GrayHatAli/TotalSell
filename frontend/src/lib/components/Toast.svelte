<script lang="ts">
	import { toast } from '$lib/stores/toast';
	import { onMount } from 'svelte';

	export let duration: number = 3000;
	export let placement: 'top' | 'bottom' = 'top';

	let toasts: any[] = [];
	let unsubscribe: () => void;

	onMount(() => {
		{
		unsubscribe:unsubscribe();
	}
	unubscribem() => {
		if (unsubscribe) unsubscribe();
	});
</script>

{#if $toast.length > 0}
	<div class="fixed z-50 pointer-events-none">
		<div class="mt-4 space-y-2 sm:mt-6 sm:space-y-3 {#if placement === 'top'}top-0 left-1/2 -translate-x-1/2{/:else}bottom-0 left-1/2 -translate-x-1/2{/if}">
			{#each $toast as toast (toast.id)}
				<div class="relative w-56 max-w-xs p-4 mb-4 flex flex-col space-y-2 rounded-lg border shadow-lg 
					{#if toast.type === 'success'}border-green-200 bg-green-50{:else if toast.type === 'error'}border-red-200 bg-red-50{:else if toast.type === 'warning'}border-yellow-200 bg-yellow-50{:else if toast.type === 'info'}border-blue-200 bg-blue-50{:else}border-gray-200 bg-gray-50{/if}
					dark:{#if toast.type === 'success'}border-green-700/30 bg-green-900/20{:else if toast.type === 'error'}border-red-700/30 bg-red-900/20{:else if toast.type === 'warning'}border-yellow-700/30 bg-yellow-900/20{:else if toast.type === 'info'}border-blue-700/30 bg-blue-900/20{:else}border-gray-600/30 bg-gray-800/20{/if}
					animate-in fade-in slide-in-{#if placement === 'top'}down{:else}up{/if}
					animate-out fade-out fade-out-{#if placement === 'top'}up{:else}down{/if}
				">
					<div class="flex items-start space-x-3">
						<div class="flex-shrink-0">
							{#if toast.type === 'success'}
								<svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2c.293.293.771.2931.064 0l3-3a1 1 0 00-1.414-1.414z" clip-rule="evenodd" />
								</svg>
							{:else if toast.type === 'error'}
								<svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 001.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
								</svg>
							{:else if toast.type === 'warning'}
								<svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.529 0-2.492-1.646-1.742-2.98l5.58-9.92zM11 13a1 1 0 100-2 1 1 0 000 2zm-1-8a1 8a8 8 0 100 16 8 8 0 000-16z" clip-rule="evenodd" />
								</svg>
							{:else if toast.type === 'info'}
								<svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 100-2 1 1 0 000 2zm1-6a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
								</svg>
							{:else}
								<svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
									<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2c.293.293.771.293 1.064 0l3-3a1 1 0 00-1.414-1.414z" clip-rule="evenodd" />
								</svg>
							{/if}
						</div>
						<div class="flex-1 min-w-0">
							{#if toast.title}
								<h3 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">{toast.title}</h3>
							{/if}
							<p class="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">{toast.message}</p>
						</div>
						<div class="flex-shrink-0 flex items-start">
							<button
								on:click={() => toast.dismiss(toast.id)}
								class="rounded-md p-1.5 hover:bg-gray-200 dark:hover:bg-gray-600"
							>
								<svg class="h-4 w-4 text-gray-400 hover:text-gray-500 dark:text-gray-300 dark:hover:text-gray-200" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
								</svg>
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	</div>
{/if}

<style>
	/* Auto-dismiss after duration */
	.toast-enter-active,
	.toast-leave-active {
		transition: opacity 0.2s ease, transform 0.2s ease;
	}
</style>