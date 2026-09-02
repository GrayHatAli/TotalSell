import { apiRequest, normalizeList, type ListResponse } from './client';

export interface Category {
	id: number;
	name: string;
	slug?: string | null;
	parent_id?: number | null;
	image_url?: string | null;
	active: boolean;
	created_at: string;
	updated_at: string;
}

export type CategoryPayload = Omit<Category, 'id' | 'created_at' | 'updated_at'>;

export interface CategoryParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listCategories(params: CategoryParams = {}): Promise<ListResponse<Category>> {
	const query = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') query.set(k, String(v)); });
	return normalizeList<Category>(await apiRequest<Category[]>(`/categories?${query}`));
}

export async function createCategory(data: Partial<CategoryPayload>): Promise<Category> {
	const body = await apiRequest<Category>('/categories', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create category');
	return body.data;
}

export async function updateCategory(id: number, data: Partial<CategoryPayload>): Promise<Category> {
	const body = await apiRequest<Category>(`/categories/${id}`, {
		method: 'PATCH',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to update category');
	return body.data;
}

export async function deleteCategory(id: number): Promise<void> {
	const body = await apiRequest(`/categories/${id}`, {
		method: 'DELETE'
	});
	if (!body.success) throw new Error(body.error?.message || 'Failed to delete category');
}
