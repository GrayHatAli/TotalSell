import { apiRequest } from '$lib/api/client';

export interface Payment {
	id: number;
	reference_type: string;
	reference_id: number;
	amount: number;
	method: string;
	bank_account_id?: number;
	date: string;
	note?: string;
	created_at: string;
	updated_at: string;
}

export interface PaymentCreate {
	reference_type: string;
	reference_id: number;
	amount: number;
	method: string;
	bank_account_id?: number;
	date: string;
	note?: string;
}

export async function listPayments(params: Record<string, string | number | undefined>): Promise<{ items: Payment[]; total: number; page: number; page_size: number }> {
	const qs = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') qs.set(k, String(v)); });
	const body = await apiRequest<any>(`/payments?${qs.toString()}`);
	return {
		items: (body?.data || []) as Payment[],
		total: (body?.meta?.total as number) || 0,
		page: (body?.meta?.page as number) || 1,
		page_size: (body?.meta?.page_size as number) || 20,
	};
}

export async function createPayment(payload: PaymentCreate): Promise<Payment> {
	const body = await apiRequest<any>('/payments', {
		method: 'POST',
		body: JSON.stringify(payload),
	});
	if (!body?.data) throw new Error('Failed to create payment');
	return body.data as Payment;
}
