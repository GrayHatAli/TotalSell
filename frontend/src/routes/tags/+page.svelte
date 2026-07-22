<script lang="ts">
	import { onMount } from 'svelte';
	import { t, locale } from '$lib/i18n';
	import { listTags, createTag, updateTag, deleteTag, type Tag } from '$lib/api/tags';

	let tags: Tag[] = [];
	let loading = false;
	let error = '';
	let search = '';
	let showModal = false;
	let editingTag: Tag | null = null;
	let formData = { name: '' };

	async function loadTags() {
		loading = true;
		error = '';
		try {
			const response = await listTags();
			tags = response.filter(t => !search || t.name.toLowerCase().includes(search.toLowerCase()));
		} catch (e) {
			error = String(e);
		} finally {
			loading = false;
		}
	}

	onMount(loadTags);

	function openAddModal() {
		editingTag = null;
		formData = { name: '' };
		showModal = true;
	}

	function openEditModal(tag: Tag) {
		editingTag = tag;
		formData = { name: tag.name };
		showModal = true;
	}

	async function handleSubmit() {
		try {
			if (editingTag) {
				await updateTag(editingTag.id, formData);
			} else {
				await createTag(formData);
			}
			showModal = false;
			loadTags();
		} catch (e) {
			error = String(e);
		}
	}

	async function handleDelete(id: number) {
		if (!confirm(t('common.delete') + '?')) return;
		try {
			await deleteTag(id);
			loadTags();
		} catch (e) {
			error = String(e);
		}
	}

	$: filteredTags = tags.filter(t => !search || t.name.toLowerCase().includes(search.toLowerCase()));
</script>

{#key $locale}
<div class="space-y-4">
	<div class="flex items-center justify-between gap-4">
		<h1 class="text-2xl font-bold">{t('nav.tags')}</h1>
		<div class="flex items-center gap-2">
			<input
				type="text"
				placeholder="{t('common.search')}..."
				class="input"
				bind:value={search}
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
					<th>{t('tags.name')}</th>
					<th>{t('common.actions')}</th>
				</tr>
			</thead>
			<tbody>
				{#if loading}
					<tr>
						<td colspan="2" class="text-center py-8">{t('common.loading')}</td>
					</tr>
				{:else if !filteredTags || filteredTags.length === 0}
					<tr>
						<td colspan="2" class="text-center py-8">{t('common.noResults')}</td>
					</tr>
				{:else}
					{#each filteredTags as tag}
						<tr>
							<td>{tag.name}</td>
							<td>
								<div class="flex gap-2">
									<button class="btn btn-sm" on:click={() => openEditModal(tag)}>
										{t('common.edit')}
									</button>
									<button class="btn btn-sm variant-filled-error" on:click={() => handleDelete(tag.id)}>
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
				{editingTag ? t('tags.edit') : t('tags.add')}
			</h2>
			<div class="space-y-4">
				<div>
					<label class="block text-sm font-medium mb-1" for="tag-name">{t('tags.name')}</label>
					<input id="tag-name" type="text" class="input w-full" bind:value={formData.name} required />
				</div>
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