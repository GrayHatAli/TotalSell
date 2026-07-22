<script lang="ts">
	import { onMount } from 'svelte';
	import { createJournalEntry } from '$lib/api/journalEntries';
	import { listAccounts } from '$lib/api/accounts';
	import { t, locale } from '$lib/i18n';

	let accounts: { id: number; code: string; name: string }[] = [];
	let description = '';
	let lines: { account_id: number; debit: number; credit: number; note?: string }[] = [];
	let error = '';

	function addLine() {
		lines = [...lines, { account_id: 0, debit: 0, credit: 0 }];
	}

	function removeLine(idx: number) {
		lines = lines.filter((_, i) => i !== idx);
	}

	$: totalDebit = lines.reduce((s, l) => s + (Number(l.debit) || 0), 0);
	$: totalCredit = lines.reduce((s, l) => s + (Number(l.credit) || 0), 0);
	$: balanced = lines.length > 0 && totalDebit === totalCredit;

	onMount(async () => {
		accounts = await listAccounts();
	});

	async function handleSave() {
		try {
			await createJournalEntry({
				date: new Date().toISOString(),
				description: description || undefined,
				lines,
			});
			lines = [];
			description = '';
			error = '';
			alert('Journal entry saved');
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to save';
		}
	}
</script>

{#key $locale}
<div class="max-w-3xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Manual Journal Entry</h1>

	{#if error}
		<div class="p-3 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded-lg text-sm">
			{error}
		</div>
	{/if}

	<div class="card p-6 space-y-4">
		<label class="space-y-1">
			<span class="text-sm font-medium">Description</span>
			<input class="input w-full" bind:value={description} />
		</label>

		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<h3 class="font-semibold">Lines</h3>
				<button class="btn btn-sm variant-soft" on:click={addLine}>Add Line</button>
			</div>
			{#each lines as line, idx}
				<div class="grid grid-cols-12 gap-2 items-end p-3 bg-surface-100 dark:bg-surface-800 rounded">
					<label class="col-span-5 space-y-1">
						<span class="text-xs font-medium">Account</span>
						<select class="select w-full" bind:value={line.account_id}>
							<option value={0}>Select account</option>
							{#each accounts as a}
								<option value={a.id}>{a.code} — {a.name}</option>
							{/each}
						</select>
					</label>
					<label class="col-span-3 space-y-1">
						<span class="text-xs font-medium">Debit</span>
						<input class="input w-full" type="number" bind:value={line.debit} min="0" />
					</label>
					<label class="col-span-3 space-y-1">
						<span class="text-xs font-medium">Credit</span>
						<input class="input w-full" type="number" bind:value={line.credit} min="0" />
					</label>
					<button class="col-span-1 btn btn-sm variant-soft-error" on:click={() => removeLine(idx)}>×</button>
				</div>
			{/each}
		</div>

		<div class="flex items-center justify-between text-sm">
			<div>Total Debit: {totalDebit.toLocaleString()}</div>
			<div>Total Credit: {totalCredit.toLocaleString()}</div>
			<div class={balanced ? 'text-success-700 dark:text-success-300' : 'text-error-700 dark:text-error-300'}>
				{balanced ? 'Balanced' : 'Not balanced'}
			</div>
		</div>

		<div class="flex justify-end">
			<button class="btn btn-primary" disabled={!balanced} on:click={handleSave}>Save Entry</button>
		</div>
	</div>
</div>
{/key}