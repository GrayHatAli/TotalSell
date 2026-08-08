<script lang="ts">
	import { toast } from '$lib/stores/toast';
	import Toast from './Toast.svelte';
	import { onMount } from 'svelte';

	let toasts: any[] = [];
	let unsubscribe: () => void;

	onMount(() => {
		unsubscribe = toast.subscribe((value: any) => {
			toasts = value;
		});
	});

	function handleClose(event: CustomEvent<{ id: string }>) {
		toast.dismiss(event.detail.id);
	}
</script>

{#each toasts as toastItem (toastItem.id)}
	<Toast
		message={toastItem.message}
		title={toastItem.title}
		type={toastItem.type}
		duration={toastItem.duration || 3000}
		placement="top"
		on:close={(e) => toast.dismiss(toastItem.id)}
		{id=toastItem.id}
	/>
{/each}