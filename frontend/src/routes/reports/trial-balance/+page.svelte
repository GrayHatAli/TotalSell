<script lang="ts">
	import { onMount } from 'svelte';
	import { getTrialBalance } from '$lib/api/reports';
	import { t, locale } from '$lib/i18n';

	let rows: any[] = [];
	let loading = true;
	let date = '';

	onMount(async () => {
		rows = await getTrialBalance(date || undefined);
		loading = false;
	});
</script>

{#key $locale}
<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Trial Balance</h1>
	<label class="space-y-1">
		<span class="text-sm font-medium">As of date</span>
		<input class="input" type="date" bind:value={date} on:change={() => { loading = true; getTrialBalance(date || undefined).then(r => { rows = r; loading = false; }); }} />
	</label>

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else}
		<div class="card overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th>Code</th>
						<th>Name</th>
						<th>Debit</th>
						<th>Credit</th>
						<th>Balance</th>
					</tr>
				</thead>
				<tbody>
					{#each rows as r}
						<tr>
							<td>{r.code}</td>
							<td>{r.name}</td>
							<td>{Number(r.debit).toLocaleString()}</td>
							<td>{Number(r.credit).toLocaleString()}</td>
							<td>{Number(r.balance).toLocaleString()}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
{/key}