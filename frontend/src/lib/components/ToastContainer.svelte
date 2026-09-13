<script lang="ts">
	import { toast } from '$lib/stores/toast';
	import type { Toast as ToastItem } from '$lib/stores/toast';
	import Toast from './Toast.svelte';
	import { onMount } from 'svelte';
	import { dir } from '$lib/i18n';

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
	<!-- Bottom inline-end corner: bottom-left in Persian (rtl), bottom-right in English. -->
	<div class="fixed bottom-4 z-50 space-y-2 pointer-events-none {$dir === 'rtl' ? 'left-4' : 'right-4'}">
		{#each toasts as toastItem (toastItem.id)}
			<div class="pointer-events-auto">
				<Toast
					id={toastItem.id}
					message={toastItem.message}
					title={toastItem.title}
					type={toastItem.type}
					duration={toastItem.duration ?? 3000}
					placement="bottom"
					on:close={handleClose}
				/>
			</div>
		{/each}
	</div>
{/if}
