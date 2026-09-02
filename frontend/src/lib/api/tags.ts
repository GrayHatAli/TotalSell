import { apiRequest, normalizeList } from './client';

export interface Tag {
	id: number;
	name: string;
	color?: string | null;
}

export type TagPayload = Omit<Tag, 'id'>;

export async function listTags(): Promise<Tag[]> {
	const { items } = normalizeList<Tag>(await apiRequest<Tag[]>('/tags'));
	return items;
}

export async function createTag(data: Partial<TagPayload>): Promise<Tag> {
	const body = await apiRequest<Tag>('/tags', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create tag');
	return body.data;
}

export async function updateTag(id: number, data: Partial<TagPayload>): Promise<Tag> {
	const body = await apiRequest<Tag>(`/tags/${id}`, {
		method: 'PATCH',
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
