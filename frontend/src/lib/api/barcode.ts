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

export interface OnlineBarcodeProduct {
	name: string;
	brand?: string | null;
	image_url?: string | null;
	quantity?: string | null;
	category?: string | null;
	source?: string | null;
}

export interface OnlineBarcodeLookupResult {
	found: boolean;
	local: boolean;
	source?: string | null;
	product?: OnlineBarcodeProduct | null;
}

export async function barcodeLookup(code: string): Promise<BarcodeLookupResult> {
	const qs = `?code=${encodeURIComponent(code)}`;
	const body = await apiRequest<any>(`/products/barcode-lookup${qs}`);
	if (!body?.data) throw new Error('Product not found');
	return body.data;
}

/**
 * Look up a barcode against the local catalog first and, if missing, against
 * online sources (Open Food Facts + optional barcodeNest fallback, both proxied
 * by the backend). Never throws for "not found" — callers inspect `found`.
 */
export async function onlineBarcodeLookup(code: string): Promise<OnlineBarcodeLookupResult> {
	const qs = `?code=${encodeURIComponent(code)}`;
	const body = await apiRequest<OnlineBarcodeLookupResult>(`/products/barcode-lookup-online${qs}`);
	return (
		body?.data ?? {
			found: false,
			local: false,
			source: null,
			product: null
		}
	);
}
