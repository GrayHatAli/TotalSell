<script lang="ts">
	import { onMount } from 'svelte';
	import { getSalesReport } from '$lib/api/reports';
	import { t, locale } from '$lib/i18n';

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
			data = await getSalesReport(fromDate, toDate);
		} catch (e) {
			data = null;
		} finally {
			loading = false;
		}
	}

	function exportExcel() {
		const url = `/reports/sales/excel?from_date=${encodeURIComponent(fromDate)}&to_date=${encodeURIComponent(toDate)}`;
		window.open(url, '_blank');
	}
</script>

{#key $locale}
<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Sales Report</h1>
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
		<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
			<div class="card p-4">
				<h3 class="font-semibold mb-2">Total Revenue</h3>
				<p class="text-xl font-mono">{Number(data.total_revenue).toLocaleString()}</p>
			</div>
			<div class="card p-4">
				<h3 class="font-semibold mb-2">Invoices</h3>
				<p class="text-xl font-mono">{data.invoice_count}</p>
			</div>
		</div>

		<div class="card overflow-x-auto mt-6">
			<h3 class="font-semibold mb-4">By Product</h3>
			<table class="table">
				<thead><tr><th>Product</th><th>Total</th><th>Qty</th></tr></thead>
				<tbody>
					{#each data.by_product as row}
						<tr><td>{row.name}</td><td>{Number(row.total).toLocaleString()}</td><td>{Number(row.quantity).toLocaleString()}</td></tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
{/key}