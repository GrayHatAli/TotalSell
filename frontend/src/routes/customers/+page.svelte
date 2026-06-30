<script lang="ts">
	import { onMount } from 'svelte';
	import { t } from '$lib/i18n';
	import { listCustomers, createCustomer, updateCustomer, deleteCustomer, type Customer } from '$lib/api/customers';

	let customers: Customer[] = [];
	let loading = false;
	let error = '';
	let search = '';
	let showModal = false;
	let editingCustomer: Customer | null = null;
	let formData = {
		name: '',
		phone: '',
		email: '',
		group: '',
		credit_limit: '',
		is_active: true
	};

	async function loadCustomers() {
		loading = true;
		error = '';
		try {
			const response = await listCustomers({ search });
			customers = response.items;
		} catch (e) {
			error = String(e);
		} finally {
			loading = false;
		}
	}

	onMount(loadCustomers);

	function openAddModal() {
		editingCustomer = null;
		formData = { name: '', phone: '', email: '', group: '', credit_limit: '', is_active: true };
		showModal = true;
	}

	function openEditModal(customer: Customer) {
		editingCustomer = customer;
		formData = {
			name: customer.name,
			phone: customer.phone || '',
			email: customer.email || '',
			group: customer.group || '',
			credit_limit: customer.credit_limit?.toString() || '',
			is_active: customer.is_active
		};
		showModal = true;
	}

	async function handleSubmit() {
		try {
			const data = {
				name: formData.name,
				phone: formData.phone || undefined,
				email: formData.email || undefined,
				group: formData.group || undefined,
				credit_limit: formData.credit_limit ? parseFloat(formData.credit_limit) : undefined,
				is_active: formData.is_active
			};
			if (editingCustomer) {
				await updateCustomer(editingCustomer.id, data);
			} else {
				await createCustomer(data);
			}
			showModal = false;
			loadCustomers();
		} catch (e) {
			error = String(e);
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.delete') + '?')) return;
		try {
			await deleteCustomer(id);
			loadCustomers();
		} catch (e) {
			error = String(e);
		}
	}

	function debounce<T extends (...args: unknown[]) => void>(fn: T, delay: number) {
		let timeout: ReturnType<typeof setTimeout>;
		return (...args: Parameters<T>) => {
			clearTimeout(timeout);
			timeout = setTimeout(() => fn(...args), delay);
		};
	}

	const onSearch = debounce(() => loadCustomers(), 300);
</script>

<div class="space-y-4">
	<div class="flex items-center justify-between gap-4">
		<h1 class="text-2xl font-bold">{t('nav.customers')}</h1>
		<div class="flex items-center gap-2">
			<input
				type="text"
				placeholder="{t('common.search')}..."
				class="input"
				bind:value={search}
				on:input={onSearch}
			/>
			<button class="btn btn-primary" on:click={openAddModal}>
				{t('common.add')}
			</button>
		</div>
	</div>

	{#if error}
		<div class="alert variant-filled-error">{t('common.error')}: {error}</div>
	{/if}

	<div class="card p-0">
		<table class="table">
			<thead>
				<tr>
					<th>{t('customers.name')}</th>
					<th>{t('customers.phone')}</th>
					<th>{t('customers.email')}</th>
					<th>{t('customers.group')}</th>
					<th>{t('customers.creditLimit')}</th>
					<th>{t('customers.active')}</th>
					<th>{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					<tr>
						<td colspan="7" class="text-center py-8">{t('common.loading')}</td>
					</tr>
				{:else if customers.length === 0}
					<tr>
						<td colspan="7" class="text-center py-8">{t('common.noResults')}</td>
					</tr>
				{:else}
					{#each customers as customer}
						<tr>
							<td>{customer.name}</td>
							<td>{customer.phone || '—'}</td>
							<td>{customer.email || '—'}</td>
							<td>{customer.group || '—'}</td>
							<td>{customer.credit_limit?.toLocaleString() || '—'}</td>
							<td>
								<span class="badge {customer.is_active ? 'variant-filled-success' : 'variant-filled-error'}">
									{customer.is_active ? t('customers.active') : t('common.cancel')}
								</span>
							</td>
							<td>
								<div class="flex gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(customer)}>
										{t('common.edit')}
									</button>
									<button class="btn btn-sm variant-filled-error" on:click={() => handleDelete(customer.id)}>
										{t('common.delete')}
									</button>
								</div>
							</td>
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</div>
</div>

{#if showModal}
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_static_element_interactions -->
	<div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
		<div class="card w-full max-w-md p-6">
			<h2 class="text-xl font-bold mb-4">
				{editingCustomer ? t('customers.edit') : t('customers.add')}
			</h2>
			<div class="space-y-4">
				<div>
					<label class="block text-sm font-medium mb-1" for="cust-name">{t('customers.name')}</label>
					<input id="cust-name" type="text" class="input w-full" bind:value={formData.name} required />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="cust-phone">{t('customers.phone')}</label>
					<input id="cust-phone" type="text" class="input w-full" bind:value={formData.phone} />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="cust-email">{t('customers.email')}</label>
					<input id="cust-email" type="email" class="input w-full" bind:value={formData.email} />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="cust-group">{t('customers.group')}</label>
					<input id="cust-group" type="text" class="input w-full" bind:value={formData.group} />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="cust-credit">{t('customers.creditLimit')}</label>
					<input id="cust-credit" type="number" class="input w-full" bind:value={formData.credit_limit} step="0.01" />
				</div>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={formData.is_active} />
					<span>{t('customers.active')}</span>
				</label>
			</div>
			<div class="flex justify-end gap-2 mt-6">
				<button class="btn" on:click={() => showModal = false}>
					{t('common.cancel')}
				</button>
				<button class="btn btn-primary" on:click={handleSubmit}>
					{t('common.save')}
				</button>
			</div>
		</div>
	</div>
{/if}
