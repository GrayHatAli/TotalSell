<script lang="ts">
	import { onMount } from 'svelte';
	import { listInventoryMovements } from '$lib/api/inventory';
	import { listProducts } from '$lib/api/products';
	import { t } from '$lib/i18n';

	let movements: any[] = [];
	let productsMap: Record<number, string> = {};
	let loading = true;
	let error = '';
	let productId = '';

	onMount(async () => {
		const [mov, prods] = await Promise.all([
			listInventoryMovements({ page: 1, page_size: 100 }),
			listProducts({ page: 1, page_size: 200 }),
		]);
		movements = mov.items;
		prods.items.forEach((p: any) => (productsMap[p.id] = p.name));
		loading = false;
	});

	$: filtered = productId ? movements.filter((m) => m.product_id === Number(productId)) : movements;
</script>

<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">{t('nav.inventory')}</h1>

	{#if error}
		<div class="p-3 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded-lg text-sm">
			{error}
		</div>
	{/if}

	<div class="flex items-center gap-4">
		<label class="space-y-1">
			<span class="text-sm font-medium">Filter by product</span>
			<select class="select" bind:value={productId}>
				<option value="">All products</option>
				{#each Object.entries(productsMap) as [id, name]}
					<option value={id}>{name}</option>
				{/each}
			</select>
		</label>
	</div>

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else}
		<div class="card overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th>#</th>
						<th>Product</th>
						<th>Type</th>
						<th>Qty</th>
						<th>Unit Cost</th>
						<th>Reference</th>
						<th>Note</th>
						<th>Date</th>
					</tr>
				</thead>
				<tbody>
					{#each filtered as m}
						<tr>
							<td>{m.id}</td>
							<td>{productsMap[m.product_id] || m.product_id}</td>
							<td>
								<span class="badge {m.movement_type === 'IN' ? 'variant-filled-success' : m.movement_type === 'OUT' ? 'variant-filled-error' : 'variant-filled-warning'}">
									{m.movement_type}
								</span>
							</td>
							<td>{Number(m.quantity).toLocaleString()}</td>
							<td>{Number(m.unit_cost).toLocaleString()}</td>
							<td>{m.reference_type || '—'} #{m.reference_id || '—'}</td>
							<td>{m.note || '—'}</td>
							<td>{m.created_at?.slice(0, 10)}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
