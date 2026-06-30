import { apiRequest } from './client';

export interface Product {
	id: number;
	name: string;
	sku?: string;
	description?: string;
	price?: number;
	cost?: number;
	category_id?: number;
	category_name?: string;
	tags?: string[];
	is_active: boolean;
}

export interface ProductListResponse {
	items: Product[];
	total: number;
	page: number;
	page_size: number;
}

export interface ProductParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listProducts(params: ProductParams = {}): Promise<ProductListResponse> {
	const query = new URLSearchParams(params as Record<string, string>);
	const body = await apiRequest<ProductListResponse>(`/products?${query}`);
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to fetch products');
	return body.data;
}

export async function createProduct(data: Omit<Product, 'id' | 'category_name'>): Promise<Product> {
	const body = await apiRequest<Product>('/products', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create product');
	return body.data;
}

export async function updateProduct(id: number, data: Partial<Omit<Product, 'id'>>): Promise<Product> {
	const body = await apiRequest<Product>(`/products/${id}`, {
		method: 'PUT',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to update product');
	return body.data;
}

export async function deleteProduct(id: number): Promise<void> {
	const body = await apiRequest(`/products/${id}`, {
		method: 'DELETE'
	});
	if (!body.success) throw new Error(body.error?.message || 'Failed to delete product');
}
