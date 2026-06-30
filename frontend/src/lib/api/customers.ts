import { apiRequest } from './client';

export interface Customer {
	id: number;
	name: string;
	phone?: string;
	email?: string;
	group?: string;
	credit_limit?: number;
	is_active: boolean;
}

export interface CustomerListResponse {
	items: Customer[];
	total: number;
	page: number;
	page_size: number;
}

export interface CustomerParams {
	search?: string;
	page?: number;
	page_size?: number;
}

export async function listCustomers(params: CustomerParams = {}): Promise<CustomerListResponse> {
	const query = new URLSearchParams(params as Record<string, string>);
	const body = await apiRequest<CustomerListResponse>(`/customers?${query}`);
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to fetch customers');
	return body.data;
}

export async function createCustomer(data: Omit<Customer, 'id'>): Promise<Customer> {
	const body = await apiRequest<Customer>('/customers', {
		method: 'POST',
		body: JSON.stringify(data)
	});
	if (!body.success || !body.data) throw new Error(body.error?.message || 'Failed to create customer');
	return body.data;
}

export async function updateCustomer(id: number, data: Partial<Omit<Customer, 'id'>>): Promise<Customer> {
	const body = await apiRequest<Customer>(`/customers/${id}`, {
		method: 'PUT',
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
