<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { toast } from '$lib/stores/toast';
	import { listTags, createTag, updateTag, deleteTag, importTags, type Tag } from '$lib/api/tags';

	let tags: Tag[] = [];
	let loading = false;
	let search = '';
	let showModal = false;
	let saving = false;
	let editingTag: Tag | null = null;
	let formData = { name: '', color: '' };
	let showImport = false;
	let importing = false;
	let importFile: File | null = null;
	let importError = '';
	let importResult: { created: number; skipped: number; failed: number; errors: { row: number; reason: string }[] } | null = null;
	let selected: number[] = [];

	function toggleSelected(id: number) {
		selected = selected.includes(id) ? selected.filter((s) => s !== id) : [...selected, id];
	}

	function allFilteredSelected(): boolean {
		return filteredTags.length > 0 && filteredTags.every((t) => selected.includes(t.id));
	}

	function toggleSelectAll() {
		if (allFilteredSelected()) {
			selected = selected.filter((id) => !filteredTags.some((t) => t.id === id));
		} else {
			selected = [...new Set([...selected, ...filteredTags.map((t) => t.id)])];
		}
	}

	async function deleteSelected() {
		if (selected.length === 0) return;
		if (!confirm(t('common.confirmDelete'))) return;
		const ids = [...selected];
		const results = await Promise.allSettled(ids.map((id) => deleteTag(id)));
		const failedCount = results.filter((r) => r.status === 'rejected').length;
		if (failedCount === 0) {
			toast.success(t('toast.deleteSuccess'));
		} else {
			toast.error(t('common.deleteFailed'), t('common.error'));
		}
		selected = [];
		await loadTags();
	}

	function errMessage(e: unknown): string {
		return e instanceof Error ? e.message : String(e);
	}

	async function loadTags() {
		loading = true;
		try {
			tags = await listTags();
			selected = [];
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

	function openImportModal() {
		importResult = null;
		importError = '';
		importFile = null;
		showImport = true;
	}

	function closeImportModal() {
		showImport = false;
	}

	function onImportFileSelected(file: File | null) {
		importFile = file;
		importResult = null;
		importError = '';
	}

	async function handleImport() {
		if (!importFile) {
			importError = t('tags.selectedFile');
			return;
		}
		importing = true;
		importError = '';
		try {
			importResult = await importTags(importFile);
			await loadTags();
		} catch (e) {
			importError = errMessage(e);
		} finally {
			importing = false;
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
			{#if selected.length > 0}
				<button class="btn btn-danger" on:click={deleteSelected}>
					{t('common.deleteSelected')} ({selected.length})
				</button>
			{/if}
			<button class="btn" on:click={openImportModal}>
				<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 6l4 0v-4l3 4v4l3-4v-4l3 4v4l4 0M9 6h2l2 6h2M13 14h1M14 14v-4" /></svg>
				{t('tags.importExcel')}
			</button>
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
					<th class="w-10">
						<input type="checkbox" checked={allFilteredSelected()} on:change={toggleSelectAll} aria-label={t('common.selectPage')} />
					</th>
					<th>{t('tags.name')}</th>
					<th>{t('tags.color')}</th>
					<th class="!text-end">{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					{#each Array(3) as _}
						<tr>
							{#each Array(4) as __}
								<td><div class="skeleton h-5 w-full"></div></td>
							{/each}
						</tr>
					{/each}
				{:else if filteredTags.length === 0}
					<tr><td colspan="4"><div class="empty-state"><p class="text-sm font-medium">{t('common.noResults')}</p></div></td></tr>
				{:else}
					{#each filteredTags as tag}
						<tr>
							<td>
								<input
									type="checkbox"
									checked={selected.includes(tag.id)}
									on:change={() => toggleSelected(tag.id)}
									aria-label={t('common.deleteSelected')}
								/>
							</td>
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
	<div class="modal-overlay">
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

{#if showImport}
	<div class="modal-overlay">
		<div class="modal-panel max-w-md p-6" role="dialog" aria-modal="true">
			<h2 class="text-lg font-bold">{t('tags.importTitle')}</h2>
			<p class="mt-1 text-sm text-muted">{t('tags.importDescription')}</p>
			<div class="mt-4 space-y-4">
				<label class="mb-1 block text-sm font-medium" for="tag-import-file">{t('tags.chooseFile')}</label>
				<input
					id="tag-import-file"
					type="file"
					accept=".xlsx,.xlsm"
					class="input"
					on:change={(e) => {
						const target = e.currentTarget as HTMLInputElement;
						onImportFileSelected(target.files?.[0] ?? null);
					}}
				/>
				<p class="text-sm text-muted">
					{importFile ? importFile.name : t('tags.selectedFile')}
				</p>
				{#if importError}
					<div class="p-2 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded text-sm">
						{importError}
					</div>
				{/if}
				{#if importResult}
					<div class="p-3 rounded border text-sm space-y-1" style="border-color: var(--app-border);">
						<p class="font-semibold">{t('tags.importDone')}</p>
						<p class="text-success-700 dark:text-success-300">{t('tags.importCreated')}: {importResult.created}</p>
						<p class="text-muted">{t('tags.importSkipped')}: {importResult.skipped}</p>
						{#if importResult.failed > 0}
							<p class="text-error-700 dark:text-error-300">{t('tags.importFailed')}: {importResult.failed}</p>
							<ul class="list-disc ps-5 text-xs">
								{#each importResult.errors as err}
									<li>Row {err.row}: {err.reason}</li>
								{/each}
							</ul>
						{/if}
					</div>
				{/if}
			</div>
			<div class="mt-6 flex justify-end gap-2">
				<button class="btn" on:click={closeImportModal} disabled={importing}>{t('common.cancel')}</button>
				<button class="btn btn-primary" on:click={handleImport} disabled={importing || !importFile}>
					{importing ? t('tags.importing') : t('common.save')}
				</button>
			</div>
		</div>
	</div>
{/if}
{/key}
