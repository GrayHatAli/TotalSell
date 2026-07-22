<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { listProducts, createProduct, updateProduct, deleteProduct, type Product } from '$lib/api/products';
	import { listCategories, type Category } from '$lib/api/categories';

	let products: Product[] = [];
	let categories: Category[] = [];
	let loading = false;
	let error = '';
	let search = '';
	let showModal = false;
	let editingProduct: Product | null = null;
	let formData = {
		name: '',
		sku: '',
		description: '',
		price: '',
		cost: '',
		category_id: '',
		tags: '',
		is_active: true
	};

	async function loadProducts() {
		loading = true;
		error = '';
		try {
			const response = await listProducts({ search });
			products = response.items;
		} catch (e) {
			error = String(e);
		} finally {
			loading = false;
		}
	}

	async function loadCategories() {
		try {
			const response = await listCategories();
			categories = response.items;
		} catch (e) {
			// ignore
		}
	}

	onMount(() => {
		loadProducts();
		loadCategories();
	});

	function openAddModal() {
		editingProduct = null;
		formData = { name: '', sku: '', description: '', price: '', cost: '', category_id: '', tags: '', is_active: true };
		showModal = true;
	}

	function openEditModal(product: Product) {
		editingProduct = product;
		formData = {
			name: product.name,
			sku: product.sku || '',
			description: product.description || '',
			price: product.price?.toString() || '',
			cost: product.cost?.toString() || '',
			category_id: product.category_id?.toString() || '',
			tags: product.tags?.join(', ') || '',
			is_active: product.is_active
		};
		showModal = true;
	}

	async function handleSubmit() {
		try {
			const data = {
				name: formData.name,
				sku: formData.sku || undefined,
				description: formData.description || undefined,
				price: formData.price ? parseFloat(formData.price) : undefined,
				cost: formData.cost ? parseFloat(formData.cost) : undefined,
				category_id: formData.category_id ? parseInt(formData.category_id) : undefined,
				tags: formData.tags ? formData.tags.split(',').map(t => t.trim()).filter(t => t) : [],
				is_active: formData.is_active
			};
			if (editingProduct) {
				await updateProduct(editingProduct.id, data);
			} else {
				await createProduct(data);
			}
			showModal = false;
			loadProducts();
		} catch (e) {
			error = String(e);
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.delete') + '?')) return;
		try {
			await deleteProduct(id);
			loadProducts();
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

	const onSearch = debounce(() => loadProducts(), 300);
</script>

{#key $locale}
<div class="space-y-4">
	<div class="flex items-center justify-between gap-4">
		<h1 class="text-2xl font-bold">{t('nav.products')}</h1>
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
					<th>{t('products.name')}</th>
					<th>{t('products.sku')}</th>
					<th>{t('products.price')}</th>
					<th>{t('products.cost')}</th>
					<th>{t('products.category')}</th>
					<th>{t('products.tags')}</th>
					<th>{t('products.active')}</th>
					<th>{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					<tr>
						<td colspan="8" class="text-center py-8">{t('common.loading')}</td>
					</tr>
				{:else if !products || products.length === 0}
					<tr>
						<td colspan="8" class="text-center py-8">{t('common.noResults')}</td>
					</tr>
				{:else}
					{#each products as product}
						<tr>
							<td>{product.name}</td>
							<td>{product.sku || '—'}</td>
							<td>{product.price?.toLocaleString() || '—'}</td>
							<td>{product.cost?.toLocaleString() || '—'}</td>
							<td>{product.category_name || '—'}</td>
							<td>{product.tags?.join(', ') || '—'}</td>
							<td>
								<span class="badge {product.is_active ? 'variant-filled-success' : 'variant-filled-error'}">
									{product.is_active ? t('products.active') : t('common.cancel')}
								</span>
							</td>
							<td>
								<div class="flex gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(product)}>
										{t('common.edit')}
									</button>
									<button class="btn btn-sm variant-filled-error" on:click={() => handleDelete(product.id)}>
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
				{editingProduct ? t('products.edit') : t('products.add')}
			</h2>
			<div class="space-y-4">
				<div>
					<label class="block text-sm font-medium mb-1" for="prod-name">{t('products.name')}</label>
					<input id="prod-name" type="text" class="input w-full" bind:value={formData.name} required />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="prod-sku">{t('products.sku')}</label>
					<input id="prod-sku" type="text" class="input w-full" bind:value={formData.sku} />
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="prod-desc">{t('products.description')}</label>
					<textarea id="prod-desc" class="input w-full" bind:value={formData.description}></textarea>
				</div>
				<div class="grid grid-cols-2 gap-4">
					<div>
						<label class="block text-sm font-medium mb-1" for="prod-price">{t('products.price')}</label>
						<input id="prod-price" type="number" class="input w-full" bind:value={formData.price} step="0.01" />
					</div>
					<div>
						<label class="block text-sm font-medium mb-1" for="prod-cost">{t('products.cost')}</label>
						<input id="prod-cost" type="number" class="input w-full" bind:value={formData.cost} step="0.01" />
					</div>
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="prod-cat">{t('products.category')}</label>
					<select id="prod-cat" class="select w-full" bind:value={formData.category_id}>
						<option value="">{t('categories.none')}</option>
						{#each categories as cat}
							<option value={cat.id}>{cat.name}</option>
						{/each}
					</select>
				</div>
				<div>
					<label class="block text-sm font-medium mb-1" for="prod-tags">{t('products.tags')}</label>
					<input id="prod-tags" type="text" class="input w-full" bind:value={formData.tags} placeholder="tag1, tag2" />
				</div>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={formData.is_active} />
					<span>{t('products.active')}</span>
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