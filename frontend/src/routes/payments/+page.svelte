<script lang="ts">
	import { onMount } from 'svelte';
	import { listPayments, createPayment } from '$lib/api/payments';
	import { listBankAccounts } from '$lib/api/bankAccounts';
	import { t, locale } from '$lib/i18n';

	let payments: { items: any[]; total: number; page: number; page_size: number } = { items: [], total: 0, page: 1, page_size: 20 };
	let accounts: any[] = [];
	let loading = true;
	let error = '';
	let page = 1;

	let showModal = false;
	let form = {
		reference_type: 'SALE',
		reference_id: 0,
		amount: 0,
		method: 'cash',
		bank_account_id: undefined as number | undefined,
		date: new Date().toISOString().slice(0, 10),
		note: '',
	};

	onMount(async () => {
		payments = await listPayments({ page: 1, page_size: 50 });
		accounts = await listBankAccounts();
		loading = false;
	});

	async function handleSave() {
		try {
			await createPayment({
				reference_type: form.reference_type,
				reference_id: Number(form.reference_id),
				amount: Number(form.amount),
				method: form.method,
				bank_account_id: form.bank_account_id,
				date: form.date,
				note: form.note || undefined,
			});
			showModal = false;
			payments = await listPayments({ page: 1, page_size: 50 });
		} catch (e) {
			error = e instanceof Error ? e.message : 'Failed to create';
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
		<h1 class="text-2xl font-bold">{t('nav.payments') || 'Payments'}</h1>
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
						<th>#</th>
						<th>Ref Type</th>
						<th>Ref ID</th>
						<th>Amount</th>
						<th>Method</th>
						<th>Account</th>
						<th>Date</th>
					</tr>
				</thead>
				<tbody>
				{#each payments.items as p}
					<tr>
						<td>{p.id}</td>
						<td>{p.reference_type}</td>
						<td>{p.reference_id}</td>
						<td>{Number(p.amount).toLocaleString()}</td>
						<td>{p.method}</td>
						<td>{accounts.find((a) => a.id === p.bank_account_id)?.name || '—'}</td>
						<td>{p.date ? p.date.slice(0, 10) : ''}</td>
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
		aria-label="Close payment dialog"
		on:click={closeModalFromBackdrop}
		on:keydown={closeModalFromKeyboard}
	>
		<div class="card p-6 w-full max-w-lg space-y-4">
			<h2 class="text-xl font-semibold">Record Payment</h2>
			<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
				<label class="space-y-1">
					<span class="text-sm font-medium">Reference Type</span>
					<select class="select w-full" bind:value={form.reference_type}>
						<option value="SALE">Sale</option>
						<option value="PURCHASE">Purchase</option>
					</select>
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Reference ID</span>
					<input class="input w-full" type="number" bind:value={form.reference_id} min="1" />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Amount</span>
					<input class="input w-full" type="number" bind:value={form.amount} min="0" step="1000" />
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Method</span>
					<select class="select w-full" bind:value={form.method}>
						<option value="cash">Cash</option>
						<option value="bank">Bank</option>
					</select>
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Bank Account</span>
					<select class="select w-full" bind:value={form.bank_account_id}>
						<option value={undefined}>None</option>
						{#each accounts as a}
							<option value={a.id}>{a.name}</option>
						{/each}
					</select>
				</label>
				<label class="space-y-1">
					<span class="text-sm font-medium">Date</span>
					<input class="input w-full" type="date" bind:value={form.date} required />
				</label>
			</div>
			<label class="space-y-1">
				<span class="text-sm font-medium">Note</span>
				<textarea class="textarea w-full" bind:value={form.note}></textarea>
			</label>
			<div class="flex justify-end gap-2">
				<button class="btn variant-soft" on:click={() => (showModal = false)}>{t('common.cancel')}</button>
				<button class="btn btn-primary" on:click={handleSave}>{t('common.save')}</button>
			</div>
		</div>
	</div>
{/if}
{/key}
