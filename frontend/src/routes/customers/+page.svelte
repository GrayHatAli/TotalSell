<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { toast } from '$lib/stores/toast';
	import { listCustomers, createCustomer, updateCustomer, deleteCustomer, type Customer } from '$lib/api/customers';

	let customers: Customer[] = [];
	let loading = false;
	let search = '';
	let showModal = false;
	let saving = false;
	let editingCustomer: Customer | null = null;
	let formData = {
		name: '',
		phone: '',
		email: '',
		customer_group: '',
		credit_limit: '',
		active: true
	};

	function errMessage(e: unknown): string {
		return e instanceof Error ? e.message : String(e);
	}

	async function loadCustomers() {
		loading = true;
		try {
			const response = await listCustomers({ search });
			customers = response.items;
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			loading = false;
		}
	}

	onMount(loadCustomers);

	function openAddModal() {
		editingCustomer = null;
		formData = { name: '', phone: '', email: '', customer_group: '', credit_limit: '', active: true };
		showModal = true;
	}

	function openEditModal(customer: Customer) {
		editingCustomer = customer;
		formData = {
			name: customer.name,
			phone: customer.phone || '',
			email: customer.email || '',
			customer_group: customer.customer_group || '',
			credit_limit: customer.credit_limit?.toString() || '',
			active: customer.active
		};
		showModal = true;
	}

	function closeModal() {
		showModal = false;
	}

	async function handleSubmit() {
		if (!formData.name.trim()) {
			toast.error(t('validation.nameRequired'), t('common.error'));
			return;
		}
		saving = true;
		try {
			const data = {
				name: formData.name.trim(),
				phone: formData.phone || undefined,
				email: formData.email || undefined,
				customer_group: formData.customer_group || undefined,
				credit_limit: formData.credit_limit ? parseFloat(formData.credit_limit) : undefined,
				active: formData.active
			};
			if (editingCustomer) {
				await updateCustomer(editingCustomer.id, data);
				toast.success(t('toast.updateSuccess'));
			} else {
				await createCustomer(data);
				toast.success(t('toast.createSuccess'));
			}
			showModal = false;
			await loadCustomers();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			saving = false;
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.confirmDelete'))) return;
		try {
			await deleteCustomer(id);
			toast.success(t('toast.deleteSuccess'));
			await loadCustomers();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
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

{#key $locale}
<div class="space-y-5">
	<div class="page-header">
		<div>
			<h1 class="text-2xl font-bold tracking-tight">{t('nav.customers')}</h1>
			<p class="mt-0.5 text-sm text-muted">{t('customers.subtitle')}</p>
		</div>
		<div class="flex items-center gap-2">
			<input
				type="text"
				placeholder="{t('common.search')}..."
				class="input !w-56"
				bind:value={search}
				on:input={onSearch}
			/>
			<button class="btn btn-primary" on:click={openAddModal}>
				<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
				</svg>
				{t('common.add')}
			</button>
		</div>
	</div>

	<div class="card overflow-hidden">
		<table class="table">
			<thead>
				<tr>
					<th>{t('customers.name')}</th>
					<th>{t('customers.phone')}</th>
					<th>{t('customers.email')}</th>
					<th>{t('customers.group')}</th>
					<th>{t('customers.creditLimit')}</th>
					<th>{t('customers.active')}</th>
					<th class="!text-end">{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					{#each Array(3) as _}
						<tr>
							{#each Array(7) as __}
								<td><div class="skeleton h-5 w-full"></div></td>
							{/each}
						</tr>
					{/each}
				{:else if customers.length === 0}
					<tr>
						<td colspan="7">
							<div class="empty-state">
								<svg class="h-10 w-10 opacity-40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
								</svg>
								<p class="text-sm font-medium">{t('common.noResults')}</p>
							</div>
						</td>
					</tr>
				{:else}
					{#each customers as customer}
						<tr>
							<td class="font-semibold">{customer.name}</td>
							<td>{customer.phone || '—'}</td>
							<td>{customer.email || '—'}</td>
							<td>{customer.customer_group || '—'}</td>
							<td>{customer.credit_limit?.toLocaleString() ?? '—'}</td>
							<td>
								<span class="badge {customer.active ? 'variant-filled-success' : 'variant-filled-error'}">
									{customer.active ? t('customers.active') : t('customers.inactive')}
								</span>
							</td>
							<td>
								<div class="flex justify-end gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(customer)}>
										{t('common.edit')}
									</button>
									<button class="btn btn-sm btn-danger" on:click={() => handleDelete(customer.id)}>
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
	<div class="modal-overlay" on:click={(e) => { if (e.target === e.currentTarget) closeModal(); }}>
		<div class="modal-panel max-w-md p-6" role="dialog" aria-modal="true">
			<h2 class="text-lg font-bold">
				{editingCustomer ? t('customers.edit') : t('customers.add')}
			</h2>
			<div class="mt-4 space-y-4">
				<div>
					<label class="mb-1 block text-sm font-medium" for="cust-name">{t('customers.name')} *</label>
					<input id="cust-name" type="text" class="input" bind:value={formData.name} required />
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="cust-phone">{t('customers.phone')}</label>
						<input id="cust-phone" type="text" class="input" bind:value={formData.phone} />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="cust-email">{t('customers.email')}</label>
						<input id="cust-email" type="email" class="input" bind:value={formData.email} />
					</div>
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="cust-group">{t('customers.group')}</label>
						<input id="cust-group" type="text" class="input" bind:value={formData.customer_group} />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="cust-credit">{t('customers.creditLimit')}</label>
						<input id="cust-credit" type="number" class="input" bind:value={formData.credit_limit} step="0.01" min="0" />
					</div>
				</div>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input type="checkbox" bind:checked={formData.active} />
					<span>{t('customers.active')}</span>
				</label>
			</div>
			<div class="mt-6 flex justify-end gap-2">
				<button class="btn" on:click={closeModal} disabled={saving}>
					{t('common.cancel')}
				</button>
				<button class="btn btn-primary" on:click={handleSubmit} disabled={saving}>
					{saving ? t('common.saving') : t('common.save')}
				</button>
			</div>
		</div>
	</div>
{/if}
{/key}
