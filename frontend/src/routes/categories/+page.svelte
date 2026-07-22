<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { listCategories, createCategory, updateCategory, deleteCategory, type Category } from '$lib/api/categories';

	let categories: Category[] = [];
	let loading = false;
	let error = '';
	let search = '';
	let showModal = false;
	let editingCategory: Category | null = null;
	let formData = {
		name: '',
		slug: '',
		parent_id: '',
		is_active: true
	};

	async function loadCategories() {
		loading = true;
		error = '';
		try {
			const response = await listCategories({ search });
			categories = response.items;
		} catch (e) {
			error = String(e);
		} finally {
			loading = false;
		}
	}

	onMount(loadCategories);

	function openAddModal() {
		editingCategory = null;
		formData = { name: '', slug: '', parent_id: '', is_active: true };
		showModal = true;
	}

	function openEditModal(category: Category) {
		editingCategory = category;
		formData = {
			name: category.name,
			slug: category.slug,
			parent_id: category.parent_id?.toString() || '',
			is_active: category.is_active
		};
		showModal = true;
	}

	async function handleSubmit() {
		try {
			const data = {
				name: formData.name,
				slug: formData.slug,
				parent_id: formData.parent_id ? parseInt(formData.parent_id) : undefined,
				is_active: formData.is_active
			};
			if (editingCategory) {
				await updateCategory(editingCategory.id, data);
			} else {
				await createCategory(data);
			}
			showModal = false;
			loadCategories();
		} catch (e) {
			error = String(e);
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.delete') + '?')) return;
		try {
			await deleteCategory(id);
			loadCategories();
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

	const onSearch = debounce(() => loadCategories(), 300);

	function getParentName(parentId: number | null | undefined): string {
		if (!parentId) return t('categories.none');
		const parent = categories.find(c => c.id === parentId);
		return parent?.name || t('categories.none');
	}
</script>

{#key $locale}
<div class="space-y-4">
	<div class="flex items-center justify-between gap-4">
		<h1 class="text-2xl font-bold">{t('nav.categories')}</h1>
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
					<th>{t('categories.name')}</th>
					<th>{t('categories.slug')}</th>
					<th>{t('categories.parent')}</th>
					<th>{t('categories.active')}</th>
					<th>{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					<tr>
						<td colspan="5" class="text-center py-8">{t('common.loading')}</td>
					</tr>
				{:else if categories.length === 0}
					<tr>
						<td colspan="5" class="text-center py-8">{t('common.noResults')}</td>
					</tr>
				{:else}
					{#each categories as category}
						<tr>
							<td>{category.name}</td>
							<td>{category.slug}</td>
							<td>{getParentName(category.parent_id)}</td>
							<td>
								<span class="badge {category.is_active ? 'variant-filled-success' : 'variant-filled-error'}">
									{category.is_active ? t('categories.active') : t('common.cancel')}
								</span>
							</td>
							<td>
								<div class="flex gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(category)}>
										{t('common.edit')}
									</button>
									<button class="btn btn-sm variant-filled-error" on:click={() => handleDelete(category.id)}>
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
				{editingCategory ? t('categories.edit') : t('categories.add')}
			</h2>
			<div class="space-y-4">
				<div>
					<label class="block text-sm font-medium mb-1" for="cat-name">{t('categories.name')}</label>
					<input id="cat-name" type="text" class="input w-full" bind:value={formData.name} required />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="cat-slug">{t('categories.slug')}</label>
					<input id="cat-slug" type="text" class="input w-full" bind:value={formData.slug} required />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="cat-parent">{t('categories.parent')}</label>
					<select id="cat-parent" class="select w-full" bind:value={formData.parent_id}>
						<option value="">{t('categories.none')}</option>
						{#each categories as cat}
							{#if !editingCategory || cat.id !== editingCategory.id}
								<option value={cat.id}>{cat.name}</option>
							{/if}
						{/each}
					</select>
				</div>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={formData.is_active} />
					<span>{t('categories.active')}</span>
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
{/key}