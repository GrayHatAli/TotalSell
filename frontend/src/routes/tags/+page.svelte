<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { toast } from '$lib/stores/toast';
	import { listTags, createTag, updateTag, deleteTag, type Tag } from '$lib/api/tags';

	let tags: Tag[] = [];
	let loading = false;
	let search = '';
	let showModal = false;
	let saving = false;
	let editingTag: Tag | null = null;
	let formData = { name: '', color: '' };

	function errMessage(e: unknown): string {
		return e instanceof Error ? e.message : String(e);
	}

	async function loadTags() {
		loading = true;
		try {
			tags = await listTags();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			loading = false;
		}
	}

	onMount(loadTags);

	function openAddModal() {
		editingTag = null;
		formData = { name: '', color: '' };
		showModal = true;
	}

	function openEditModal(tag: Tag) {
		editingTag = tag;
		formData = { name: tag.name, color: tag.color || '' };
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
			const data = { name: formData.name.trim(), color: formData.color || undefined };
			if (editingTag) {
				await updateTag(editingTag.id, data);
				toast.success(t('toast.updateSuccess'));
			} else {
				await createTag(data);
				toast.success(t('toast.createSuccess'));
			}
			showModal = false;
			await loadTags();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		} finally {
			saving = false;
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.confirmDelete'))) return;
		try {
			await deleteTag(id);
			toast.success(t('toast.deleteSuccess'));
			await loadTags();
		} catch (e) {
			toast.error(errMessage(e), t('common.error'));
		}
	}

	$: filteredTags = tags.filter(
		(tag) => !search || tag.name.toLowerCase().includes(search.toLowerCase())
	);
</script>

{#key $locale}
<div class="space-y-5">
	<div class="page-header">
		<div>
			<h1 class="text-2xl font-bold tracking-tight">{t('nav.tags')}</h1>
			<p class="mt-0.5 text-sm text-muted">{t('tags.subtitle')}</p>
		</div>
		<div class="flex items-center gap-2">
			<input type="text" placeholder="{t('common.search')}..." class="input !w-56" bind:value={search} />
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
					<th>{t('tags.name')}</th>
					<th>{t('tags.color')}</th>
					<th class="!text-end">{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					{#each Array(3) as _}
						<tr>
							{#each Array(3) as __}
								<td><div class="skeleton h-5 w-full"></div></td>
							{/each}
						</tr>
					{/each}
				{:else if filteredTags.length === 0}
					<tr><td colspan="3"><div class="empty-state"><p class="text-sm font-medium">{t('common.noResults')}</p></div></td></tr>
				{:else}
					{#each filteredTags as tag}
						<tr>
							<td class="font-semibold">{tag.name}</td>
							<td>
								{#if tag.color}
									<span class="badge variant-filled-primary">
										<span class="h-2.5 w-2.5 rounded-full" style="background: {tag.color}"></span>
										{tag.color}
									</span>
								{:else}
									—
								{/if}
							</td>
							<td>
								<div class="flex justify-end gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(tag)}>{t('common.edit')}</button>
									<button class="btn btn-sm btn-danger" on:click={() => handleDelete(tag.id)}>{t('common.delete')}</button>
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
		<div class="modal-panel max-w-sm p-6" role="dialog" aria-modal="true">
			<h2 class="text-lg font-bold">{editingTag ? t('tags.edit') : t('tags.add')}</h2>
			<div class="mt-4 space-y-4">
				<div>
					<label class="mb-1 block text-sm font-medium" for="tag-name">{t('tags.name')} *</label>
					<input id="tag-name" type="text" class="input" bind:value={formData.name} required />
				</div>
				<div>
					<label class="mb-1 block text-sm font-medium" for="tag-color">{t('tags.color')}</label>
					<input id="tag-color" type="color" class="input !h-10 !w-20 !p-1" bind:value={formData.color} />
				</div>
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
