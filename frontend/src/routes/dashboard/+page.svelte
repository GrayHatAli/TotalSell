<script lang="ts">
	import { onMount } from 'svelte';
	import { currentUser } from '$lib/stores/auth';
	import { locale, t } from '$lib/i18n';
	import { listCustomers } from '$lib/api/customers';
	import { listProducts } from '$lib/api/products';
	import { listSaleInvoices } from '$lib/api/saleInvoices';
	import { getInventoryReport, getSalesReport } from '$lib/api/reports';

	let loading = true;
	let error = '';
	let metrics = {
		customers: 0,
		products: 0,
		invoices: 0,
		revenue: 0,
		lowStock: 0
	};

	function formatDate(date: Date) {
		const year = date.getFullYear();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		return `${year}-${month}-${day}`;
	}

	async function loadDashboard() {
		loading = true;
		error = '';
		const today = new Date();
		const thirtyDaysAgo = new Date(today);
		thirtyDaysAgo.setDate(today.getDate() - 30);

		const results = await Promise.allSettled([
			listCustomers({ page: 1, page_size: 1 }),
			listProducts({ page: 1, page_size: 1 }),
			listSaleInvoices({ page: 1, page_size: 1 }),
			getInventoryReport(),
			getSalesReport(formatDate(thirtyDaysAgo), formatDate(today))
		]);

		const [customers, products, invoices, inventory, sales] = results;
		metrics = {
			customers: customers.status === 'fulfilled' ? customers.value.total : metrics.customers,
			products: products.status === 'fulfilled' ? products.value.total : metrics.products,
			invoices: invoices.status === 'fulfilled' ? invoices.value.total : metrics.invoices,
			revenue: sales.status === 'fulfilled' ? sales.value.total_revenue : metrics.revenue,
			lowStock: inventory.status === 'fulfilled' ? inventory.value.low_stock_count : metrics.lowStock
		};

		const failedRequest = results.find((result) => result.status === 'rejected');
		if (failedRequest?.status === 'rejected') {
			error = failedRequest.reason instanceof Error ? failedRequest.reason.message : t('dashboard.loadError');
		}
		loading = false;
	}

	onMount(loadDashboard);

	$: _locale = $locale;
	$: metricCards = _locale
		? [
				{ label: t('nav.customers'), value: metrics.customers.toLocaleString(), detail: t('dashboard.activeRelationships'), color: '#0f766e', href: '/customers' },
				{ label: t('nav.products'), value: metrics.products.toLocaleString(), detail: t('dashboard.catalogItems'), color: '#2563eb', href: '/products' },
				{ label: t('nav.sales'), value: metrics.invoices.toLocaleString(), detail: t('dashboard.saleInvoices'), color: '#b7791f', href: '/sales' },
				{ label: t('reports.totalRevenue'), value: metrics.revenue.toLocaleString(), detail: t('dashboard.lastThirtyDays'), color: '#15803d', href: '/reports/sales' },
				{ label: t('reports.lowStock'), value: metrics.lowStock.toLocaleString(), detail: t('reports.needsAttention'), color: '#be123c', href: '/reports/inventory' }
			]
		: [];
</script>

{#key $locale}
<div class="mx-auto max-w-7xl space-y-6">
	<div class="grid gap-4 lg:grid-cols-[minmax(0,1fr)_22rem]">
		<section class="card overflow-hidden p-6 sm:p-8">
			<div class="max-w-3xl">
				<p class="text-sm font-black uppercase text-muted">{$currentUser?.email ? `Signed in as ${$currentUser.email}` : 'Owner workspace'}</p>
				<h1 class="mt-3 text-3xl font-black tracking-tight sm:text-4xl">{t('dashboard.welcome')}</h1>
				<p class="mt-3 max-w-2xl text-base leading-7 text-muted">
					{t('dashboard.description')}
				</p>
			</div>

			<div class="mt-8 grid gap-3 sm:grid-cols-4">
				<a class="btn btn-primary justify-start" href="/sales">{t('sales.add')}</a>
				<a class="btn justify-start" href="/purchases">{t('purchases.add')}</a>
				<a class="btn justify-start" href="/reports">{t('reports.title')}</a>
				<button class="btn justify-start" on:click={loadDashboard} disabled={loading}>{t('dashboard.refresh')}</button>
			</div>
		</section>

		<aside class="card p-5">
			<h2 class="text-sm font-black uppercase text-muted">{t('dashboard.operationalFlow')}</h2>
			<div class="mt-5 space-y-3">
				<a href="/sales" class="flex gap-3 rounded-md p-1 transition hover:bg-teal-50">
					<span class="mt-1 h-2.5 w-2.5 rounded-full bg-teal-600"></span>
					<p class="text-sm"><strong>{t('dashboard.invoices')}</strong> {t('dashboard.invoicesDescription')}</p>
				</a>
				<a href="/reports" class="flex gap-3 rounded-md p-1 transition hover:bg-amber-50">
					<span class="mt-1 h-2.5 w-2.5 rounded-full bg-amber-600"></span>
					<p class="text-sm"><strong>{t('reports.title')}</strong> {t('dashboard.reportsDescription')}</p>
				</a>
				<a href="/reports/inventory" class="flex gap-3 rounded-md p-1 transition hover:bg-rose-50">
					<span class="mt-1 h-2.5 w-2.5 rounded-full bg-rose-600"></span>
					<p class="text-sm"><strong>{t('reports.lowStock')}</strong> {t('dashboard.lowStockDescription')}</p>
				</a>
			</div>
		</aside>
	</div>

	{#if error}
		<div class="alert variant-filled-error">{error}</div>
	{/if}

	<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-5">
		{#each metricCards as metric}
			<a href={metric.href} class="metric-card block transition hover:-translate-y-0.5 hover:shadow-xl" style={`--metric-color: ${metric.color};`}>
				<p class="text-sm font-bold text-muted">{metric.label}</p>
				<p class="mt-3 text-3xl font-black tracking-tight">{loading ? '...' : metric.value}</p>
				<p class="mt-2 text-xs font-semibold uppercase text-muted">{metric.detail}</p>
			</a>
		{/each}
	</div>

	<div class="grid gap-4 lg:grid-cols-3">
		<a href="/products" class="card p-5 transition hover:-translate-y-0.5 hover:shadow-xl">
			<h3 class="text-lg font-black">{t('nav.products')}</h3>
			<p class="mt-2 text-sm leading-6 text-muted">{t('dashboard.productsDescription')}</p>
		</a>
		<a href="/accounting/journal-entries" class="card p-5 transition hover:-translate-y-0.5 hover:shadow-xl">
			<h3 class="text-lg font-black">{t('accounting.journalEntries')}</h3>
			<p class="mt-2 text-sm leading-6 text-muted">{t('dashboard.ledgerDescription')}</p>
		</a>
		<a href="/inventory" class="card p-5 transition hover:-translate-y-0.5 hover:shadow-xl">
			<h3 class="text-lg font-black">{t('nav.inventory')}</h3>
			<p class="mt-2 text-sm leading-6 text-muted">{t('dashboard.inventoryDescription')}</p>
		</a>
	</div>
</div>
{/key}
