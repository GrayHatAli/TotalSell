<script lang="ts">
	import { onMount } from 'svelte';
	import { listJournalEntries } from '$lib/api/journalEntries';
	import { t } from '$lib/i18n';

	let entries: any[] = [];
	let loading = true;
	let error = '';

	onMount(async () => {
		try {
			const resp = await listJournalEntries({});
			entries = resp.items;
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load';
		} finally {
			loading = false;
		}
	});
</script>

<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">{t('nav.accounting')}</h1>

	{#if error}
		<div class="p-3 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded-lg text-sm">
			{error}
		</div>
	{/if}

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else if entries.length === 0}
		<p>{t('common.noResults')}</p>
	{:else}
		<div class="card overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th>#</th>
						<th>Date</th>
						<th>Description</th>
						<th>Ref Type</th>
						<th>Ref ID</th>
					</tr>
				</thead>
				<tbody>
					{#each entries as e}
						<tr>
							<td>{e.entry_id || e.id}</td>
							<td>{e.date ? e.date.slice(0, 10) : ''}</td>
							<td>{e.description || '—'}</td>
							<td>{e.reference_type || '—'}</td>
							<td>{e.reference_id || '—'}</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
