<script lang="ts">
	import { toast } from '$lib/stores/toast';
	import type { Toast as ToastItem } from '$lib/stores/toast';
	import Toast from './Toast.svelte';
	import { onMount } from 'svelte';

	let toasts: ToastItem[] = [];
	let unsubscribe: () => void;

	onMount(() => {
		unsubscribe = toast.subscribe((value) => {
			toasts = value;
		});
	});

	function handleClose(event: CustomEvent<{ id: string }>) {
		toast.dismiss(event.detail.id);
	}
</script>

{#if toasts.length > 0}
	<div class="fixed top-0 left-1/2 z-50 mt-4 -translate-x-1/2 space-y-2 pointer-events-none sm:mt-6 sm:space-y-3">
		{#each toasts as toastItem (toastItem.id)}
			<div class="pointer-events-auto">
				<Toast
					id={toastItem.id}
					message={toastItem.message}
					title={toastItem.title}
					type={toastItem.type}
					duration={toastItem.duration ?? 3000}
					placement="top"
					on:close={handleClose}
				/>
			</div>
		{/each}
	</div>
{/if}
