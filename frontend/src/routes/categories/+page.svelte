<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { toast } from '$lib/stores/toast';
	import { listCategories, createCategory, updateCategory, deleteCategory, type Category } from '$lib/api/categories';

	let categories: Category[] = [];
	let loading = false;
	let search = '';
	let showModal = false;
	let saving = false;
	let editingCategory: Category | null = null;
	let formData = {
		name: '',
		slug: '',
		parent_id: '',
		active: true
	};

	function errMessage(e: unknown): string {
		return e instanceof Error ? e.message : String(e);
	}

	async function loadCategories() {
		loading = true;
		try {
			const response = await listCategories({ search });
			categories = response.items;
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			loading = false;
		}
	}

	onMount(loadCategories);

	function openAddModal() {
		editingCategory = null;
		formData = { name: '', slug: '', parent_id: '', active: true };
		showModal = true;
	}

	function openEditModal(category: Category) {
		editingCategory = category;
		formData = {
			name: category.name,
			slug: category.slug || '',
			parent_id: category.parent_id?.toString() || '',
			active: category.active
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
				slug: formData.slug || undefined,
				parent_id: formData.parent_id ? parseInt(formData.parent_id) : undefined,
				active: formData.active
			};
			if (editingCategory) {
				await updateCategory(editingCategory.id, data);
				toast.success(t('toast.updateSuccess'));
			} else {
				await createCategory(data);
				toast.success(t('toast.createSuccess'));
			}
			showModal = false;
			await loadCategories();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			saving = false;
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.confirmDelete'))) return;
		try {
			await deleteCategory(id);
			toast.success(t('toast.deleteSuccess'));
			await loadCategories();
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

	const onSearch = debounce(() => loadCategories(), 300);

	function getParentName(parentId: number | null | undefined): string {
		if (!parentId) return t('categories.none');
		const parent = categories.find((c) => c.id === parentId);
		return parent?.name || t('categories.none');
	}
</script>

{#key $locale}
<div class="space-y-5">
	<div class="page-header">
		<div>
			<h1 class="text-2xl font-bold tracking-tight">{t('nav.categories')}</h1>
			<p class="mt-0.5 text-sm text-muted">{t('categories.subtitle')}</p>
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
					<th>{t('categories.name')}</th>
					<th>{t('categories.slug')}</th>
					<th>{t('categories.parent')}</th>
					<th>{t('categories.active')}</th>
					<th class="!text-end">{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					{#each Array(3) as _}
						<tr>
							{#each Array(5) as __}
								<td><div class="skeleton h-5 w-full"></div></td>
							{/each}
						</tr>
					{/each}
				{:else if categories.length === 0}
					<tr><td colspan="5"><div class="empty-state"><p class="text-sm font-medium">{t('common.noResults')}</p></div></td></tr>
				{:else}
					{#each categories as category}
						<tr>
							<td class="font-semibold">{category.name}</td>
							<td>{category.slug || '—'}</td>
							<td>{getParentName(category.parent_id)}</td>
							<td>
								<span class="badge {category.active ? 'variant-filled-success' : 'variant-filled-error'}">
									{category.active ? t('categories.active') : t('categories.inactive')}
								</span>
							</td>
							<td>
								<div class="flex justify-end gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(category)}>{t('common.edit')}</button>
									<button class="btn btn-sm btn-danger" on:click={() => handleDelete(category.id)}>{t('common.delete')}</button>
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
			<h2 class="text-lg font-bold">{editingCategory ? t('categories.edit') : t('categories.add')}</h2>
			<div class="mt-4 space-y-4">
				<div>
					<label class="mb-1 block text-sm font-medium" for="cat-name">{t('categories.name')} *</label>
					<input id="cat-name" type="text" class="input" bind:value={formData.name} required />
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="cat-slug">{t('categories.slug')}</label>
						<input id="cat-slug" type="text" class="input" bind:value={formData.slug} />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="cat-parent">{t('categories.parent')}</label>
						<select id="cat-parent" class="select" bind:value={formData.parent_id}>
							<option value="">{t('categories.none')}</option>
							{#each categories as cat}
								{#if !editingCategory || cat.id !== editingCategory.id}
									<option value={cat.id}>{cat.name}</option>
								{/if}
							{/each}
						</select>
					</div>
				</div>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input type="checkbox" bind:checked={formData.active} />
					<span>{t('categories.active')}</span>
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
