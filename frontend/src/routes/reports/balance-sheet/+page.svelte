<script lang="ts">
	import { onMount } from 'svelte';
	import { getBalanceSheet } from '$lib/api/reports';
	import { t, locale } from '$lib/i18n';

	let date = '';
	let data: any = null;
	let loading = true;

	onMount(async () => {
		date = new Date().toISOString().slice(0, 10);
		await load();
	});

	async function load() {
		loading = true;
		try {
			data = await getBalanceSheet(date || undefined);
		} catch (e) {
			data = null;
		} finally {
			loading = false;
		}
	}
</script>

{#key $locale}
<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Balance Sheet</h1>
	<label class="space-y-1">
		<span class="text-sm font-medium">As of date</span>
		<input class="input" type="date" bind:value={date} on:change={load} />
	</label>

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else if data}
		<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
			<div class="card p-4">
				<h3 class="font-semibold mb-2">Assets</h3>
				<p class="text-xl font-mono">{Number(data.total_assets).toLocaleString()}</p>
			</div>
			<div class="card p-4">
				<h3 class="font-semibold mb-2">Liabilities</h3>
				<p class="text-xl font-mono">{Number(data.total_liabilities).toLocaleString()}</p>
			</div>
			<div class="card p-4">
				<h3 class="font-semibold mb-2">Equity</h3>
				<p class="text-xl font-mono">{Number(data.total_equity).toLocaleString()}</p>
			</div>
		</div>
		<div class="card p-4 mt-4">
			<div class="flex justify-between">
				<span>Liabilities + Equity</span>
				<span class="font-mono">{Number(data.liabilities_plus_equity).toLocaleString()}</span>
			</div>
			<div class="flex justify-between mt-2">
				<span>Balanced</span>
				<span class={data.is_balanced ? 'text-success-700 dark:text-success-300' : 'text-error-700 dark:text-error-300'}>
					{data.is_balanced ? 'Yes' : 'No'}
				</span>
			</div>
		</div>
	{/if}
</div>
{/key}