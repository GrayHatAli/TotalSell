<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { toast } from '$lib/stores/toast';
	import { listSuppliers, createSupplier, updateSupplier, deleteSupplier, type Supplier } from '$lib/api/suppliers';

	let suppliers: Supplier[] = [];
	let loading = false;
	let search = '';
	let showModal = false;
	let saving = false;
	let editingSupplier: Supplier | null = null;
	let formData = {
		name: '',
		contact_person: '',
		phone: '',
		email: '',
		tax_id: '',
		bank_account: '',
		payment_terms: '',
		active: true
	};

	function errMessage(e: unknown): string {
		return e instanceof Error ? e.message : String(e);
	}

	async function loadSuppliers() {
		loading = true;
		try {
			const response = await listSuppliers({ search });
			suppliers = response.items;
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			loading = false;
		}
	}

	onMount(loadSuppliers);

	function openAddModal() {
		editingSupplier = null;
		formData = { name: '', contact_person: '', phone: '', email: '', tax_id: '', bank_account: '', payment_terms: '', active: true };
		showModal = true;
	}

	function openEditModal(supplier: Supplier) {
		editingSupplier = supplier;
		formData = {
			name: supplier.name,
			contact_person: supplier.contact_person || '',
			phone: supplier.phone || '',
			email: supplier.email || '',
			tax_id: supplier.tax_id || '',
			bank_account: supplier.bank_account || '',
			payment_terms: supplier.payment_terms || '',
			active: supplier.active
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
				contact_person: formData.contact_person || undefined,
				phone: formData.phone || undefined,
				email: formData.email || undefined,
				tax_id: formData.tax_id || undefined,
				bank_account: formData.bank_account || undefined,
				payment_terms: formData.payment_terms || undefined,
				active: formData.active
			};
			if (editingSupplier) {
				await updateSupplier(editingSupplier.id, data);
				toast.success(t('toast.updateSuccess'));
			} else {
				await createSupplier(data);
				toast.success(t('toast.createSuccess'));
			}
			showModal = false;
			await loadSuppliers();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			saving = false;
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.confirmDelete'))) return;
		try {
			await deleteSupplier(id);
			toast.success(t('toast.deleteSuccess'));
			await loadSuppliers();
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

	const onSearch = debounce(() => loadSuppliers(), 300);
</script>

{#key $locale}
<div class="space-y-5">
	<div class="page-header">
		<div>
			<h1 class="text-2xl font-bold tracking-tight">{t('nav.suppliers')}</h1>
			<p class="mt-0.5 text-sm text-muted">{t('suppliers.subtitle')}</p>
		</div>
		<div class="flex items-center gap-2">
			<input type="text" placeholder="{t('common.search')}..." class="input !w-56" bind:value={search} on:input={onSearch} />
			<button class="btn btn-primary" on:click={openAddModal}>
				<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
				{t('common.add')}
			</button>
		</div>
	</div>

	<div class="card overflow-hidden">
		<table class="table">
			<thead>
				<tr>
					<th>{t('suppliers.name')}</th>
					<th>{t('suppliers.contactPerson')}</th>
					<th>{t('suppliers.phone')}</th>
					<th>{t('suppliers.email')}</th>
					<th>{t('suppliers.active')}</th>
					<th class="!text-end">{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					{#each Array(3) as _}
						<tr>
							{#each Array(6) as __}
								<td><div class="skeleton h-5 w-full"></div></td>
							{/each}
						</tr>
					{/each}
				{:else if suppliers.length === 0}
					<tr><td colspan="6"><div class="empty-state"><p class="text-sm font-medium">{t('common.noResults')}</p></div></td></tr>
				{:else}
					{#each suppliers as supplier}
						<tr>
							<td class="font-semibold">{supplier.name}</td>
							<td>{supplier.contact_person || '—'}</td>
							<td>{supplier.phone || '—'}</td>
							<td>{supplier.email || '—'}</td>
							<td>
								<span class="badge {supplier.active ? 'variant-filled-success' : 'variant-filled-error'}">
									{supplier.active ? t('suppliers.active') : t('suppliers.inactive')}
								</span>
							</td>
							<td>
								<div class="flex justify-end gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(supplier)}>{t('common.edit')}</button>
									<button class="btn btn-sm btn-danger" on:click={() => handleDelete(supplier.id)}>{t('common.delete')}</button>
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
		<div class="modal-panel max-w-lg p-6" role="dialog" aria-modal="true">
			<h2 class="text-lg font-bold">{editingSupplier ? t('suppliers.edit') : t('suppliers.add')}</h2>
			<div class="mt-4 space-y-4">
				<div>
					<label class="mb-1 block text-sm font-medium" for="sup-name">{t('suppliers.name')} *</label>
					<input id="sup-name" type="text" class="input" bind:value={formData.name} required />
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="sup-contact">{t('suppliers.contactPerson')}</label>
						<input id="sup-contact" type="text" class="input" bind:value={formData.contact_person} />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="sup-phone">{t('suppliers.phone')}</label>
						<input id="sup-phone" type="text" class="input" bind:value={formData.phone} />
					</div>
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="sup-email">{t('suppliers.email')}</label>
						<input id="sup-email" type="email" class="input" bind:value={formData.email} />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="sup-tax">{t('suppliers.taxId')}</label>
						<input id="sup-tax" type="text" class="input" bind:value={formData.tax_id} />
					</div>
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="sup-bank">{t('suppliers.bankAccount')}</label>
						<input id="sup-bank" type="text" class="input" bind:value={formData.bank_account} />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="sup-terms">{t('suppliers.paymentTerms')}</label>
						<input id="sup-terms" type="text" class="input" bind:value={formData.payment_terms} />
					</div>
				</div>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input type="checkbox" bind:checked={formData.active} />
					<span>{t('suppliers.active')}</span>
				</label>
			</div>
			<div class="mt-6 flex justify-end gap-2">
				<button class="btn" on:click={closeModal} disabled={saving}>{t('common.cancel')}</button>
				<button class="btn btn-primary" on:click={handleSubmit} disabled={saving}>
					{saving ? t('common.saving') : t('common.save')}
				</button>
			</div>
		</div>
	</div>
{/if}
{/key}
