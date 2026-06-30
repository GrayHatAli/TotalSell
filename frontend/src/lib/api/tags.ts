import { apiRequest } from './client';

export interface Tag {
	id: number;
	name: string;
}

export interface TagListResponse {
	items: Tag[];
}

export async function listTags(): Promise<Tag[]> {
	const body = await apiRequest<TagListResponse>('/tags');
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to fetch tags');
	return body.data.items;
}

export async function createTag(data: Omit<Tag, 'id'>): Promise<Tag> {
	const body = await apiRequest<Tag>('/tags', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create tag');
	return body.data;
}

export async function updateTag(id: number, data: Partial<Omit<Tag, 'id'>>): Promise<Tag> {
	const body = await apiRequest<Tag>(`/tags/${id}`, {
		method: 'PUT',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to update tag');
	return body.data;
}

export async function deleteTag(id: number): Promise<void> {
	const body = await apiRequest(`/tags/${id}`, {
		method: 'DELETE'
	});
	if (!body.success) throw new Error(body.error?.message || 'Failed to delete tag');
}
