<script lang="ts">
	import { onMount } from 'svelte';
	import { getProfitLoss } from '$lib/api/reports';
	import { t } from '$lib/i18n';

	let fromDate = '';
	let toDate = '';
	let result: any = null;
	let loading = true;

	onMount(async () => {
		const today = new Date().toISOString().slice(0, 10);
		fromDate = `${new Date().getFullYear()}-01-01`;
		toDate = today;
		await load();
	});

	async function load() {
		loading = true;
		try {
			result = await getProfitLoss(fromDate, toDate);
		} catch (e) {
			result = null;
		} finally {
			loading = false;
		}
	}
</script>

<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Profit & Loss</h1>
	<div class="flex gap-4">
		<label class="space-y-1">
			<span class="text-sm font-medium">From</span>
			<input class="input" type="date" bind:value={fromDate} />
		</label>
		<label class="space-y-1">
			<span class="text-sm font-medium">To</span>
			<input class="input" type="date" bind:value={toDate} />
		</label>
		<button class="btn btn-primary mt-5" on:click={load}>Run</button>
	</div>

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else if result}
		<div class="card p-6 space-y-4">
			<div class="flex justify-between">
				<span>Total Revenue</span>
				<span class="font-mono">{Number(result.total_revenue).toLocaleString()}</span>
			</div>
			<div class="flex justify-between">
				<span>Total Expenses</span>
				<span class="font-mono">{Number(result.total_expenses).toLocaleString()}</span>
			</div>
			<div class="flex justify-between text-lg font-bold border-t pt-2">
				<span>Net Profit</span>
				<span class="font-mono">{Number(result.net_profit).toLocaleString()}</span>
			</div>
		</div>
	{/if}
</div>
