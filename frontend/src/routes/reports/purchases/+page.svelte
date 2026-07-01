<script lang="ts">
	import { onMount } from 'svelte';
	import { getPurchaseReport } from '$lib/api/reports';
	import { t } from '$lib/i18n';

	let fromDate = '';
	let toDate = '';
	let data: any = null;
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
			data = await getPurchaseReport(fromDate, toDate);
		} catch (e) {
			data = null;
		} finally {
			loading = false;
		}
	}

	function exportExcel() {
		const url = `/reports/purchases/excel?from_date=${encodeURIComponent(fromDate)}&to_date=${encodeURIComponent(toDate)}`;
		window.open(url, '_blank');
	}
</script>

<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Purchase Report</h1>
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
		<button class="btn btn-primary mt-5" on:click={exportExcel}>Export Excel</button>
	</div>

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else if data}
		<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
			<div class="card p-4">
				<h3 class="font-semibold mb-2">Total Purchases</h3>
				<p class="text-xl font-mono">{Number(data.total_purchases).toLocaleString()}</p>
			</div>
			<div class="card p-4">
				<h3 class="font-semibold mb-2">Invoices</h3>
				<p class="text-xl font-mono">{data.invoice_count}</p>
			</div>
		</div>

		<div class="card overflow-x-auto mt-6">
			<h3 class="font-semibold mb-4">By Supplier</h3>
			<table class="table">
				<thead><tr><th>Supplier</th><th>Total</th><th>Count</th></tr></thead>
				<tbody>
					{#each data.by_supplier as row}
						<tr><td>{row.name}</td><td>{Number(row.total).toLocaleString()}</td><td>{row.count}</td></tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
