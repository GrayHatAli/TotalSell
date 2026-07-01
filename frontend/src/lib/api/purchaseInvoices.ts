import { apiRequest } from '$lib/api/client';

export interface PurchaseItem {
	id: number;
	product_id?: number;
	quantity: number;
	unit_cost: number;
	discount_pct: number;
	tax_pct: number;
	line_total: number;
	note?: string;
}

export interface PurchaseInvoice {
	id: number;
	number: string;
	date: string;
	supplier_id: number;
	reference_number?: string;
	subtotal: number;
	discount_pct: number;
	discount_amount: number;
	tax_pct: number;
	tax_amount: number;
	shipping: number;
	total: number;
	payment_method?: string;
	payment_status: string;
	notes?: string;
	created_by?: number;
	journal_entry_id?: number;
	items: PurchaseItem[];
	created_at: string;
	updated_at: string;
}

export interface PurchaseInvoiceCreate {
	supplier_id: number;
	date: string;
	items: { product_id?: number; quantity: number; unit_cost: number; discount_pct?: number; tax_pct?: number; note?: string }[];
	reference_number?: string;
	discount_pct?: number;
	tax_pct?: number;
	shipping?: number;
	payment_method?: string;
	payment_status?: string;
	notes?: string;
}

export async function listPurchaseInvoices(params: Record<string, string | number | undefined>): Promise<{ items: PurchaseInvoice[]; total: number; page: number; page_size: number }> {
	const qs = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') qs.set(k, String(v)); });
	const body = await apiRequest<any>(`/purchase-invoices?${qs.toString()}`);
	return {
		items: (body?.data || []) as PurchaseInvoice[],
		total: (body?.meta?.total as number) || 0,
		page: (body?.meta?.page as number) || 1,
		page_size: (body?.meta?.page_size as number) || 20,
	};
}

export async function createPurchaseInvoice(payload: PurchaseInvoiceCreate): Promise<PurchaseInvoice> {
	const body = await apiRequest<any>('/purchase-invoices', {
		method: 'POST',
		body: JSON.stringify(payload),
	});
	if (!body?.data) throw new Error('Failed to create purchase invoice');
	return body.data as PurchaseInvoice;
}

export async function getPurchaseInvoice(id: number): Promise<PurchaseInvoice> {
	const body = await apiRequest<any>(`/purchase-invoices/${id}`);
	if (!body?.data) throw new Error('Failed to fetch purchase invoice');
	return body.data as PurchaseInvoice;
}
