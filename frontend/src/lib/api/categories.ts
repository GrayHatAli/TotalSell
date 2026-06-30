import { apiRequest } from './client';

export interface Category {
	id: number;
	name: string;
	slug: string;
	parent_id?: number | null;
	is_active: boolean;
}

export interface CategoryListResponse {
	items: Category[];
	total: number;
	page: number;
	page_size: number;
}

export interface CategoryParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listCategories(params: CategoryParams = {}): Promise<CategoryListResponse> {
	const query = new URLSearchParams(params as Record<string, string>);
	const body = await apiRequest<CategoryListResponse>(`/categories?${query}`);
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to fetch categories');
	return body.data;
}

export async function createCategory(data: Omit<Category, 'id'>): Promise<Category> {
	const body = await apiRequest<Category>('/categories', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create category');
	return body.data;
}

export async function updateCategory(id: number, data: Partial<Omit<Category, 'id'>>): Promise<Category> {
	const body = await apiRequest<Category>(`/categories/${id}`, {
		method: 'PUT',
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
