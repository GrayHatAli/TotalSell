<script lang="ts">
	import { onMount } from 'svelte';
	import { listBankAccounts, createBankAccount, updateBankAccount, deleteBankAccount } from '$lib/api/bankAccounts';
	import { t, locale } from '$lib/i18n';
	import { goto } from '$app/navigation';

	let accounts: { id: number; name: string; account_type: string; bank_name?: string; current_balance: number; active: boolean }[] = [];
	let loading = true;
	let error = '';
	let showModal = false;
	let editingId: number | null = null;
	let form = { name: '', account_type: 'bank', iban: '', account_number: '', bank_name: '', opening_balance: 0, notes: '', active: true };

	onMount(async () => {
		await load();
	});

	async function load() {
		loading = true;
		error = '';
		try {
			accounts = await listBankAccounts();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to load';
		} finally {
			loading = false;
		}
	}

	function openCreate() {
		editingId = null;
		form = { name: '', account_type: 'bank', iban: '', account_number: '', bank_name: '', opening_balance: 0, notes: '', active: true };
		showModal = true;
	}

	function openEdit(row: any) {
		editingId = row.id;
		form = { ...row };
		showModal = true;
	}

	async function handleSave() {
		try {
			if (editingId) {
				await updateBankAccount(editingId, form);
			} else {
				await createBankAccount(form);
			}
			showModal = false;
			await load();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Save failed';
		}
	}

	async function handleDelete(id: number) {
		if (!confirm('Delete this bank account?')) return;
		try {
			await deleteBankAccount(id);
			await load();
		} catch (e) {
			error = e instanceof Error ? e.message : 'Delete failed';
		}
	}

	function closeModalFromBackdrop(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			showModal = false;
		}
	}

	function closeModalFromKeyboard(event: KeyboardEvent) {
		if (event.target === event.currentTarget && ['Escape', 'Enter', ' '].includes(event.key)) {
			showModal = false;
		}
	}
</script>

{#key $locale}
<div class="max-w-5xl mx-auto space-y-6">
	<div class="flex items-center justify-between">
		<h1 class="text-2xl font-bold">{t('nav.banking') || 'Bank Accounts'}</h1>
		<button class="btn btn-primary" on:click={openCreate}>{t('common.add')}</button>
	</div>

	{#if error}
		<div class="p-3 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded-lg text-sm">
			{error}
		</div>
	{/if}

	{#if loading}
		<p>{t('common.loading')}</p>
	{:else if !accounts || accounts.length === 0}
		<p>{t('common.noResults')}</p>
	{:else}
		<div class="card overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th>Name</th>
						<th>Type</th>
						<th>Bank</th>
						<th>Balance</th>
						<th>Active</th>
						<th class="text-right">Actions</th>
					</tr>
				</thead>
				<tbody>
					{#each accounts as acc}
						<tr>
							<td class="font-medium">{acc.name}</td>
							<td>{acc.account_type}</td>
							<td>{acc.bank_name || '—'}</td>
							<td>{Number(acc.current_balance).toLocaleString()}</td>
							<td>
								<span class="badge {acc.active ? 'variant-filled-success' : 'variant-filled-error'}">{acc.active ? 'Active' : 'Inactive'}</span>
							</td>
							<td class="text-right space-x-2">
								<button class="btn btn-sm variant-soft" on:click={() => openEdit(acc)}>{t('common.edit')}</button>
								<button class="btn btn-sm variant-soft-error" on:click={() => handleDelete(acc.id)}>{t('common.delete')}</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>

{#if showModal}
	<div
		class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
		role="button"
		tabindex="0"
		aria-label="Close bank account dialog"
		on:click={closeModalFromBackdrop}
		on:keydown={closeModalFromKeyboard}
	>
		<div class="card p-6 w-full max-w-lg space-y-4">
			<h2 class="text-xl font-semibold">{editingId ? t('common.edit') : t('common.add')} Bank Account</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
				<label class="space-y-1">
					<span class="text-sm font-medium">Name</span>
					<input class="input w-full" bind:value={form.name} required />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Type</span>
					<select class="select w-full" bind:value={form.account_type}>
						<option value="bank">Bank</option>
						<option value="cash">Cash</option>
						<option value="wallet">Wallet</option>
					</select>
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Bank Name</span>
					<input class="input w-full" bind:value={form.bank_name} />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Account Number</span>
					<input class="input w-full" bind:value={form.account_number} />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">IBAN</span>
					<input class="input w-full" bind:value={form.iban} />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Opening Balance</span>
					<input class="input w-full" type="number" bind:value={form.opening_balance} />
				</label>
			</div>
			<label class="space-y-1">
				<span class="text-sm font-medium">Notes</span>
				<textarea class="textarea w-full" bind:value={form.notes}></textarea>
			</label>
			<div class="flex justify-end gap-2">
				<button class="btn variant-soft" on:click={() => (showModal = false)}>{t('common.cancel')}</button>
				<button class="btn btn-primary" on:click={handleSave}>{t('common.save')}</button>
			</div>
		</div>
	</div>
{/if}
{/key}
