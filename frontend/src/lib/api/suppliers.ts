import { apiRequest } from './client';

export interface Supplier {
	id: number;
	name: string;
	phone?: string;
	email?: string;
	address?: string;
	is_active: boolean;
}

export interface SupplierListResponse {
	items: Supplier[];
	total: number;
	page: number;
	page_size: number;
}

export interface SupplierParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listSuppliers(params: SupplierParams = {}): Promise<SupplierListResponse> {
	const query = new URLSearchParams(params as Record<string, string>);
	const body = await apiRequest<SupplierListResponse>(`/suppliers?${query}`);
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to fetch suppliers');
	return body.data;
}

export async function createSupplier(data: Omit<Supplier, 'id'>): Promise<Supplier> {
	const body = await apiRequest<Supplier>('/suppliers', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create supplier');
	return body.data;
}

export async function updateSupplier(id: number, data: Partial<Omit<Supplier, 'id'>>): Promise<Supplier> {
	const body = await apiRequest<Supplier>(`/suppliers/${id}`, {
		method: 'PUT',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to update supplier');
	return body.data;
}

export async function deleteSupplier(id: number): Promise<void> {
	const body = await apiRequest(`/suppliers/${id}`, {
		method: 'DELETE'
	});
	if (!body.success) throw new Error(body.error?.message || 'Failed to delete supplier');
}
