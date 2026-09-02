import { apiRequest, normalizeList, type ListResponse } from './client';

export interface Customer {
	id: number;
	name: string;
	phone?: string | null;
	email?: string | null;
	national_id?: string | null;
	customer_group?: string | null;
	credit_limit?: number | null;
	address?: string | null;
	notes?: string | null;
	active: boolean;
	created_at: string;
	updated_at: string;
}

export type CustomerPayload = Omit<Customer, 'id' | 'created_at' | 'updated_at'>;

export interface CustomerParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listCustomers(params: CustomerParams = {}): Promise<ListResponse<Customer>> {
	const query = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') query.set(k, String(v)); });
	return normalizeList<Customer>(await apiRequest<Customer[]>(`/customers?${query}`));
}

export async function createCustomer(data: Partial<CustomerPayload>): Promise<Customer> {
	const body = await apiRequest<Customer>('/customers', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create customer');
	return body.data;
}

export async function updateCustomer(id: number, data: Partial<CustomerPayload>): Promise<Customer> {
	const body = await apiRequest<Customer>(`/customers/${id}`, {
		method: 'PATCH',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to update customer');
	return body.data;
}

export async function deleteCustomer(id: number): Promise<void> {
	const body = await apiRequest(`/customers/${id}`, {
		method: 'DELETE'
	});
	if (!body.success) throw new Error(body.error?.message || 'Failed to delete customer');
}
