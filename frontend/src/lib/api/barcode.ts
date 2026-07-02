import { apiRequest } from './client';

export interface BarcodeLookupResult {
	id: number;
	name: string;
	sku?: string;
	barcode?: string;
	sale_price: number;
	cost_price: number;
	unit?: string;
}

export async function barcodeLookup(code: string): Promise<BarcodeLookupResult> {
	const qs = `?code=${encodeURIComponent(code)}`;
	const body = await apiRequest<any>(`/products/barcode-lookup${qs}`);
	if (!body?.data) throw new Error('Product not found');
	return body.data;
}
