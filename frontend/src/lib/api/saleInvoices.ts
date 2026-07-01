import { apiRequest } from '$lib/api/client';

export interface SaleItem {
	id: number;
	product_id?: number;
	quantity: number;
	unit_price: number;
	discount_pct: number;
	tax_pct: number;
	line_total: number;
	unit_cost?: number;
	note?: string;
}

export interface SaleInvoice {
	id: number;
	number: string;
	date: string;
	customer_id?: number;
	reference_number?: string;
	subtotal: number;
	discount_pct: number;
	discount_amount: number;
	tax_pct: number;
	tax_amount: number;
	total: number;
	payment_method?: string;
	payment_status: string;
	notes?: string;
	created_by?: number;
	journal_entry_id?: number;
	items: SaleItem[];
	created_at: string;
	updated_at: string;
}

export interface SaleInvoiceCreate {
	customer_id?: number;
	date: string;
	items: { product_id?: number; quantity: number; unit_price: number; discount_pct?: number; tax_pct?: number; note?: string }[];
	reference_number?: string;
	discount_pct?: number;
	tax_pct?: number;
	payment_method?: string;
	payment_status?: string;
	notes?: string;
}

export async function listSaleInvoices(params: Record<string, string | number | undefined>): Promise<{ items: SaleInvoice[]; total: number; page: number; page_size: number }> {
	const qs = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') qs.set(k, String(v)); });
	const body = await apiRequest<any>(`/sale-invoices?${qs.toString()}`);
	return {
		items: (body?.data || []) as SaleInvoice[],
		total: (body?.meta?.total as number) || 0,
		page: (body?.meta?.page as number) || 1,
		page_size: (body?.meta?.page_size as number) || 20,
	};
}

export async function createSaleInvoice(payload: SaleInvoiceCreate): Promise<SaleInvoice> {
	const body = await apiRequest<any>('/sale-invoices', {
		method: 'POST',
		body: JSON.stringify(payload),
	});
	if (!body?.data) throw new Error('Failed to create sale invoice');
	return body.data as SaleInvoice;
}

export async function getSaleInvoice(id: number): Promise<SaleInvoice> {
	const body = await apiRequest<any>(`/sale-invoices/${id}`);
	if (!body?.data) throw new Error('Failed to fetch sale invoice');
	return body.data as SaleInvoice;
}
