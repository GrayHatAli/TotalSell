import { apiRequest, normalizeList, type ListResponse } from './client';

export interface ProductTagRef {
	id: number;
	name: string;
	color?: string | null;
}

export interface Product {
	id: number;
	name: string;
	sku?: string | null;
	barcode?: string | null;
	category_id?: number | null;
	category_name?: string | null;
	product_type?: string | null;
	unit?: string | null;
	sale_price?: number | null;
	cost_price?: number | null;
	min_stock?: number | null;
	active: boolean;
	tags?: ProductTagRef[];
	created_at: string;
	updated_at: string;
}

export interface ProductPayload {
	name: string;
	sku?: string;
	barcode?: string;
	category_id?: number;
	product_type?: string;
	unit?: string;
	sale_price?: number;
	cost_price?: number;
	min_stock?: number;
	active?: boolean;
	tag_ids?: number[];
}

export interface ProductParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listProducts(params: ProductParams = {}): Promise<ListResponse<Product>> {
	const query = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') query.set(k, String(v)); });
	return normalizeList<Product>(await apiRequest<Product[]>(`/products?${query}`));
}

export async function createProduct(data: ProductPayload): Promise<Product> {
	const body = await apiRequest<Product>('/products', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create product');
	return body.data;
}

export async function updateProduct(id: number, data: Partial<ProductPayload>): Promise<Product> {
	const body = await apiRequest<Product>(`/products/${id}`, {
		method: 'PATCH',
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
