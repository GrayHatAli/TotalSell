<script lang="ts">
	import { onMount } from 'svelte';
	import { t } from '$lib/i18n';
	import { listSuppliers, createSupplier, updateSupplier, deleteSupplier, type Supplier } from '$lib/api/suppliers';

	let suppliers: Supplier[] = [];
	let loading = false;
	let error = '';
	let search = '';
	let showModal = false;
	let editingSupplier: Supplier | null = null;
	let formData = {
		name: '',
		phone: '',
		email: '',
		address: '',
		is_active: true
	};

	async function loadSuppliers() {
		loading = true;
		error = '';
		try {
			const response = await listSuppliers({ search });
			suppliers = response.items;
		} catch (e) {
			error = String(e);
		} finally {
			loading = false;
		}
	}

	onMount(loadSuppliers);

	function openAddModal() {
		editingSupplier = null;
		formData = { name: '', phone: '', email: '', address: '', is_active: true };
		showModal = true;
	}

	function openEditModal(supplier: Supplier) {
		editingSupplier = supplier;
		formData = {
			name: supplier.name,
			phone: supplier.phone || '',
			email: supplier.email || '',
			address: supplier.address || '',
			is_active: supplier.is_active
		};
		showModal = true;
	}

	async function handleSubmit() {
		try {
			const data = {
				name: formData.name,
				phone: formData.phone || undefined,
				email: formData.email || undefined,
				address: formData.address || undefined,
				is_active: formData.is_active
			};
			if (editingSupplier) {
				await updateSupplier(editingSupplier.id, data);
			} else {
				await createSupplier(data);
			}
			showModal = false;
			loadSuppliers();
		} catch (e) {
			error = String(e);
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.delete') + '?')) return;
		try {
			await deleteSupplier(id);
			loadSuppliers();
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

	const onSearch = debounce(() => loadSuppliers(), 300);
</script>

<div class="space-y-4">
	<div class="flex items-center justify-between gap-4">
		<h1 class="text-2xl font-bold">{t('nav.suppliers')}</h1>
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
					<th>{t('suppliers.name')}</th>
					<th>{t('suppliers.phone')}</th>
					<th>{t('suppliers.email')}</th>
					<th>{t('suppliers.address')}</th>
					<th>{t('suppliers.active')}</th>
					<th>{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					<tr>
						<td colspan="6" class="text-center py-8">{t('common.loading')}</td>
					</tr>
				{:else if suppliers.length === 0}
					<tr>
						<td colspan="6" class="text-center py-8">{t('common.noResults')}</td>
					</tr>
				{:else}
					{#each suppliers as supplier}
						<tr>
							<td>{supplier.name}</td>
							<td>{supplier.phone || '—'}</td>
							<td>{supplier.email || '—'}</td>
							<td>{supplier.address || '—'}</td>
							<td>
								<span class="badge {supplier.is_active ? 'variant-filled-success' : 'variant-filled-error'}">
									{supplier.is_active ? t('suppliers.active') : t('common.cancel')}
								</span>
							</td>
							<td>
								<div class="flex gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(supplier)}>
										{t('common.edit')}
									</button>
									<button class="btn btn-sm variant-filled-error" on:click={() => handleDelete(supplier.id)}>
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
				{editingSupplier ? t('suppliers.edit') : t('suppliers.add')}
			</h2>
			<div class="space-y-4">
				<div>
					<label class="block text-sm font-medium mb-1" for="sup-name">{t('suppliers.name')}</label>
					<input id="sup-name" type="text" class="input w-full" bind:value={formData.name} required />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="sup-phone">{t('suppliers.phone')}</label>
					<input id="sup-phone" type="text" class="input w-full" bind:value={formData.phone} />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="sup-email">{t('suppliers.email')}</label>
					<input id="sup-email" type="email" class="input w-full" bind:value={formData.email} />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="sup-address">{t('suppliers.address')}</label>
					<textarea id="sup-address" class="input w-full" bind:value={formData.address}></textarea>
				</div>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={formData.is_active} />
					<span>{t('suppliers.active')}</span>
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
