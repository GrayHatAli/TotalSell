<script lang="ts">
	import { onMount } from 'svelte';
	import { getInventoryReport } from '$lib/api/reports';
	import { t, locale } from '$lib/i18n';

	let data: any = null;
	let loading = true;

	onMount(async () => {
		try {
			data = await getInventoryReport();
		} catch (e) {
			data = null;
		} finally {
			loading = false;
		}
	});

	function exportExcel() {
		window.open('/reports/inventory/excel', '_blank');
	}
</script>

{#key $locale}
<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Inventory Report</h1>

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else if data}
		<div class="card p-4 mb-4">
			<p>Low stock items: <strong class={data.low_stock_count > 0 ? 'text-error-700 dark:text-error-300' : ''}>{data.low_stock_count}</strong></p>
		</div>

		<div class="card overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th>Product</th>
						<th>SKU</th>
						<th>Stock</th>
						<th>Min Stock</th>
						<th>Low Stock</th>
					</tr>
				</thead>
				<tbody>
					{#each data.items as item}
						<tr>
							<td>{item.name}</td>
							<td>{item.sku || '—'}</td>
							<td>{Number(item.stock).toLocaleString()}</td>
							<td>{Number(item.min_stock).toLocaleString()}</td>
							<td>
								<span class="badge {item.low_stock ? 'variant-filled-error' : 'variant-filled-success'}">
									{item.low_stock ? 'Yes' : 'No'}
								</span>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>

		<div class="mt-4">
			<button class="btn btn-primary" on:click={exportExcel}>Export Excel</button>
		</div>
	{/if}
</div>
{/key}