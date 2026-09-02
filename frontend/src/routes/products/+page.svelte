<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { toast } from '$lib/stores/toast';
	import {
		listProducts,
		createProduct,
		updateProduct,
		deleteProduct,
		type Product
	} from '$lib/api/products';
	import { listCategories, type Category } from '$lib/api/categories';
	import { listTags, type Tag } from '$lib/api/tags';

	let products: Product[] = [];
	let categories: Category[] = [];
	let tags: Tag[] = [];
	let loading = false;
	let search = '';
	let showModal = false;
	let saving = false;
	let editingProduct: Product | null = null;
	let formData = {
		name: '',
		sku: '',
		barcode: '',
		sale_price: '',
		cost_price: '',
		unit: '',
		min_stock: '',
		category_id: '',
		selectedTagIds: [] as number[],
		active: true
	};

	function errMessage(e: unknown): string {
		return e instanceof Error ? e.message : String(e);
	}

	async function loadProducts() {
		loading = true;
		try {
			const response = await listProducts({ search });
			products = response.items;
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			loading = false;
		}
	}

	async function loadReferenceData() {
		try {
			const [cats, tgs] = await Promise.all([listCategories(), listTags()]);
			categories = cats.items;
			tags = tgs;
		} catch {
			// Non-critical: dropdowns stay empty
		}
	}

	onMount(() => {
		loadProducts();
		loadReferenceData();
	});

	function openAddModal() {
		editingProduct = null;
		formData = {
			name: '',
			sku: '',
			barcode: '',
			sale_price: '',
			cost_price: '',
			unit: '',
			min_stock: '',
			category_id: '',
			selectedTagIds: [],
			active: true
		};
		showModal = true;
	}

	function openEditModal(product: Product) {
		editingProduct = product;
		formData = {
			name: product.name,
			sku: product.sku || '',
			barcode: product.barcode || '',
			sale_price: product.sale_price?.toString() || '',
			cost_price: product.cost_price?.toString() || '',
			unit: product.unit || '',
			min_stock: product.min_stock?.toString() || '',
			category_id: product.category_id?.toString() || '',
			selectedTagIds: (product.tags || []).map((t) => t.id),
			active: product.active
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
				sku: formData.sku || undefined,
				barcode: formData.barcode || undefined,
				sale_price: formData.sale_price ? parseFloat(formData.sale_price) : undefined,
				cost_price: formData.cost_price ? parseFloat(formData.cost_price) : undefined,
				unit: formData.unit || undefined,
				min_stock: formData.min_stock ? parseFloat(formData.min_stock) : undefined,
				category_id: formData.category_id ? parseInt(formData.category_id) : undefined,
				tag_ids: formData.selectedTagIds,
				active: formData.active
			};
			if (editingProduct) {
				await updateProduct(editingProduct.id, data);
				toast.success(t('toast.updateSuccess'));
			} else {
				await createProduct(data);
				toast.success(t('toast.createSuccess'));
			}
			showModal = false;
			await loadProducts();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			saving = false;
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.confirmDelete'))) return;
		try {
			await deleteProduct(id);
			toast.success(t('toast.deleteSuccess'));
			await loadProducts();
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

	const onSearch = debounce(() => loadProducts(), 300);
</script>

{#key $locale}
<div class="space-y-5">
	<div class="page-header">
		<div>
			<h1 class="text-2xl font-bold tracking-tight">{t('nav.products')}</h1>
			<p class="mt-0.5 text-sm text-muted">{t('products.subtitle')}</p>
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
					<th>{t('products.name')}</th>
					<th>{t('products.sku')}</th>
					<th>{t('products.price')}</th>
					<th>{t('products.cost')}</th>
					<th>{t('products.category')}</th>
					<th>{t('products.tags')}</th>
					<th>{t('products.active')}</th>
					<th class="!text-end">{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					{#each Array(3) as _}
						<tr>
							{#each Array(8) as __}
								<td><div class="skeleton h-5 w-full"></div></td>
							{/each}
						</tr>
					{/each}
				{:else if products.length === 0}
					<tr><td colspan="8"><div class="empty-state"><p class="text-sm font-medium">{t('common.noResults')}</p></div></td></tr>
				{:else}
					{#each products as product}
						<tr>
							<td class="font-semibold">{product.name}</td>
							<td>{product.sku || '—'}</td>
							<td>{product.sale_price?.toLocaleString() ?? '—'}</td>
							<td>{product.cost_price?.toLocaleString() ?? '—'}</td>
							<td>{product.category_name || '—'}</td>
							<td>
								{#if product.tags && product.tags.length > 0}
									<div class="flex flex-wrap gap-1">
										{#each product.tags as tag}
											<span class="badge variant-filled-primary">{tag.name}</span>
										{/each}
									</div>
								{:else}
									—
								{/if}
							</td>
							<td>
								<span class="badge {product.active ? 'variant-filled-success' : 'variant-filled-error'}">
									{product.active ? t('products.active') : t('products.inactive')}
								</span>
							</td>
							<td>
								<div class="flex justify-end gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(product)}>{t('common.edit')}</button>
									<button class="btn btn-sm btn-danger" on:click={() => handleDelete(product.id)}>{t('common.delete')}</button>
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
			<h2 class="text-lg font-bold">{editingProduct ? t('products.edit') : t('products.add')}</h2>
			<div class="mt-4 space-y-4">
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-name">{t('products.name')} *</label>
						<input id="prod-name" type="text" class="input" bind:value={formData.name} required />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-sku">{t('products.sku')}</label>
						<input id="prod-sku" type="text" class="input" bind:value={formData.sku} />
					</div>
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-barcode">{t('products.barcode')}</label>
						<input id="prod-barcode" type="text" class="input" bind:value={formData.barcode} />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-unit">{t('products.unit')}</label>
						<input id="prod-unit" type="text" class="input" bind:value={formData.unit} />
					</div>
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-price">{t('products.price')}</label>
						<input id="prod-price" type="number" class="input" bind:value={formData.sale_price} step="0.01" min="0" />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-cost">{t('products.cost')}</label>
						<input id="prod-cost" type="number" class="input" bind:value={formData.cost_price} step="0.01" min="0" />
					</div>
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-minstock">{t('products.minStock')}</label>
						<input id="prod-minstock" type="number" class="input" bind:value={formData.min_stock} step="0.01" min="0" />
					</div>
				</div>
				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label class="mb-1 block text-sm font-medium" for="prod-cat">{t('products.category')}</label>
						<select id="prod-cat" class="select" bind:value={formData.category_id}>
							<option value="">{t('categories.none')}</option>
							{#each categories as cat}
								<option value={cat.id}>{cat.name}</option>
							{/each}
						</select>
					</div>
					<div>
						<span class="mb-1 block text-sm font-medium">{t('products.tags')}</span>
						<div class="flex max-h-28 flex-wrap gap-2 overflow-y-auto rounded-xl border p-2" style="border-color: var(--app-border);">
							{#each tags as tag}
								<label class="flex items-center gap-1.5 text-xs font-medium">
									<input type="checkbox" bind:group={formData.selectedTagIds} value={tag.id} />
									{tag.name}
								</label>
							{/each}
						</div>
					</div>
				</div>
				<label class="flex items-center gap-2 text-sm font-medium">
					<input type="checkbox" bind:checked={formData.active} />
					<span>{t('products.active')}</span>
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
