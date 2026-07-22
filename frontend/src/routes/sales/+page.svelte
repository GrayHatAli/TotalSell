<script lang="ts">
	import { onMount } from 'svelte';
	import { listSaleInvoices, createSaleInvoice } from '$lib/api/saleInvoices';
	import { listCustomers } from '$lib/api/customers';
	import { listProducts } from '$lib/api/products';
	import { barcodeLookup } from '$lib/api/barcode';
	import { t, locale } from '$lib/i18n';
	import BarcodeScanner from '$lib/components/BarcodeScanner.svelte';

	let invoices: { items: any[]; total: number; page: number; page_size: number } = { items: [], total: 0, page: 1, page_size: 50 };
	let products: { items: any[]; total: number; page: number; page_size: number } = { items: [], total: 0, page: 1, page_size: 200 };
	let customers: { items: any[]; total: number; page: number; page_size: number } = { items: [], total: 0, page: 1, page_size: 50 };
	let customersList: any[] = [];
	let loading = true;
	let error = '';

	let showModal = false;
	let scannerOpen = false;
	let scanError = '';
	let form = {
		customer_id: null as number | null,
		date: new Date().toISOString().slice(0, 10),
		reference_number: '',
		discount_pct: 0,
		tax_pct: 9,
		payment_method: 'cash',
		payment_status: 'paid',
		notes: '',
		items: [] as { product_id?: number; quantity: number; unit_price: number; discount_pct: number; tax_pct: number; note?: string }[],
	};

	onMount(async () => {
		const [inv, cust, prod] = await Promise.all([
			listSaleInvoices({ page: 1, page_size: 50 }),
			listCustomers(),
			listProducts({ page: 1, page_size: 200 }),
		]);
		invoices = inv;
		customers = cust;
		products = prod;
		customersList = customers.items;
		loading = false;
	});

	function addItem() {
		form.items = [...form.items, { product_id: undefined, quantity: 1, unit_price: 0, discount_pct: 0, tax_pct: 9, note: '' }];
	}

	function removeItem(idx: number) {
		form.items = form.items.filter((_, i) => i !== idx);
	}

	async function handleScan(code: string) {
		try {
			const product = await barcodeLookup(code);
			const target = form.items[0];
			if (target) {
				target.product_id = product.id;
				target.unit_price = product.sale_price;
				form.items = [...form.items];
			}
			scannerOpen = false;
		} catch (e) {
			scanError = e instanceof Error ? e.message : 'Scan failed';
		}
	}

	async function handleSave() {
		try {
			await createSaleInvoice({
				customer_id: form.customer_id ? Number(form.customer_id) : undefined,
				date: form.date,
				reference_number: form.reference_number || undefined,
				discount_pct: form.discount_pct,
				tax_pct: form.tax_pct,
				payment_method: form.payment_method,
				payment_status: form.payment_status,
				notes: form.notes || undefined,
				items: form.items,
			});
			showModal = false;
			invoices = await listSaleInvoices({ page: 1, page_size: 50 });
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to create';
		}
	}
</script>

{#key $locale}
<div class="max-w-5xl mx-auto space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-2xl font-bold">{t('nav.sales')}</h1>
		<button class="btn btn-primary" on:click={() => (showModal = true)}>{t('common.add')}</button>
	</div>

	{#if error}
		<div class="p-3 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded-lg text-sm">
			{error}
		</div>
	{/if}

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else}
		<div class="card overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th>Number</th>
						<th>Date</th>
						<th>Customer</th>
						<th>Total</th>
						<th>Status</th>
						<th>Method</th>
					</tr>
				</thead>
				<tbody>
					{#each invoices.items as inv}
						<tr>
							<td class="font-medium">{inv.number}</td>
							<td>{inv.date ? inv.date.slice(0, 10) : ''}</td>
							<td>{customersList.find(c => c.id === inv.customer_id)?.name || '—'}</td>
							<td>{Number(inv.total).toLocaleString()}</td>
							<td>
								<span class="badge {inv.payment_status === 'paid' ? 'variant-filled-success' : inv.payment_status === 'partial' ? 'variant-filled-warning' : 'variant-filled-error'}">
									{inv.payment_status}
								</span>
							</td>
							<td>{inv.payment_method || '—'}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>

{#if showModal}
	<div class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 overflow-y-auto" on:click={(e) => { if (e.target === e.currentTarget) showModal = false; }}>
		<div class="card p-6 w-full max-w-4xl space-y-4 my-8">
			<h2 class="text-xl font-semibold">New Sale Invoice</h2>
			<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
				<label class="space-y-1">
					<span class="text-sm font-medium">Customer</span>
					<select class="select w-full" bind:value={form.customer_id}>
						<option value={null}>Walk-in</option>
						{#each customersList as c}
							<option value={c.id}>{c.name}</option>
						{/each}
					</select>
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Date</span>
					<input class="input w-full" type="date" bind:value={form.date} required />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Reference</span>
					<input class="input w-full" bind:value={form.reference_number} />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Discount %</span>
					<input class="input w-full" type="number" bind:value={form.discount_pct} min="0" max="100" />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Tax %</span>
					<input class="input w-full" type="number" bind:value={form.tax_pct} min="0" max="100" />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Payment</span>
					<select class="select w-full" bind:value={form.payment_method}>
						<option value="cash">Cash</option>
						<option value="bank">Bank</option>
						<option value="credit">Credit</option>
					</select>
				</label>
			</div>

			<div class="space-y-2">
				<div class="flex items-center justify-between">
					<h3 class="font-semibold">Items</h3>
					<div class="flex gap-2">
						<button class="btn btn-sm variant-soft" on:click={() => addItem()}>Add Item</button>
						<button class="btn btn-sm variant-soft" on:click={() => (scannerOpen = true)} disabled={(form.items ?? []).length === 0}>Scan</button>
					</div>
				</div>
				{#each form.items as item, idx}
					<div class="grid grid-cols-1 sm:grid-cols-6 gap-2 p-3 bg-surface-100 dark:bg-surface-800 rounded">
						<select class="select col-span-2" bind:value={item.product_id}>
							<option value={undefined}>Select product</option>
							{#each products.items as p}
								<option value={p.id}>{p.name}</option>
							{/each}
						</select>
						<input class="input" type="number" bind:value={item.quantity} min="1" placeholder="Qty" />
						<input class="input" type="number" bind:value={item.unit_price} min="0" step="1000" placeholder="Price" />
						<input class="input" type="number" bind:value={item.discount_pct} min="0" max="100" placeholder="Disc%" />
						<input class="input" type="number" bind:value={item.tax_pct} min="0" max="100" placeholder="Tax%" />
						<button class="btn btn-sm variant-soft-error" on:click={() => removeItem(idx)}>×</button>
					</div>
				{/each}
			</div>

			<div class="flex justify-end gap-2">
				<button class="btn variant-soft" on:click={() => (showModal = false)}>{t('common.cancel')}</button>
				<button class="btn btn-primary" on:click={handleSave} disabled={(form.items ?? []).length === 0}>{t('common.save')}</button>
			</div>
		</div>
	</div>
{/if}

{#if scannerOpen}
	<div class="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4" on:click={(e) => { if (e.target === e.currentTarget) scannerOpen = false; }}>
		<div class="card p-4 w-full max-w-md space-y-3">
			<h3 class="text-lg font-semibold">Scan Barcode</h3>
			{#if scanError}
				<div class="p-2 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded text-sm">
					{scanError}
				</div>
			{/if}
			<BarcodeScanner on:scanned={(e) => handleScan(e.detail)}></BarcodeScanner>
			<div class="flex justify-end">
				<button class="btn variant-soft" on:click={() => { scannerOpen = false; scanError = ''; }}>Close</button>
			</div>
		</div>
	</div>
{/if}
{/key}