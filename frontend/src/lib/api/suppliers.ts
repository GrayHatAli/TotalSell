import { apiRequest, normalizeList, type ListResponse } from './client';

export interface Supplier {
	id: number;
	name: string;
	contact_person?: string | null;
	phone?: string | null;
	email?: string | null;
	tax_id?: string | null;
	bank_account?: string | null;
	payment_terms?: string | null;
	notes?: string | null;
	active: boolean;
	created_at: string;
	updated_at: string;
}

export type SupplierPayload = Omit<Supplier, 'id' | 'created_at' | 'updated_at'>;

export interface SupplierParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listSuppliers(params: SupplierParams = {}): Promise<ListResponse<Supplier>> {
	const query = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') query.set(k, String(v)); });
	return normalizeList<Supplier>(await apiRequest<Supplier[]>(`/suppliers?${query}`));
}

export async function createSupplier(data: Partial<SupplierPayload>): Promise<Supplier> {
	const body = await apiRequest<Supplier>('/suppliers', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create supplier');
	return body.data;
}

export async function updateSupplier(id: number, data: Partial<SupplierPayload>): Promise<Supplier> {
	const body = await apiRequest<Supplier>(`/suppliers/${id}`, {
		method: 'PATCH',
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
