import { apiRequest } from '$lib/api/client';

export interface InventoryMovement {
	id: number;
	product_id: number;
	movement_type: string;
	quantity: number;
	unit_cost: number;
	reference_type?: string;
	reference_id?: number;
	note?: string;
	created_at: string;
}

export async function listInventoryMovements(params: Record<string, string | number | undefined>): Promise<{ items: InventoryMovement[]; total: number; page: number; page_size: number }> {
	const qs = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') qs.set(k, String(v)); });
	const body = await apiRequest<any>(`/inventory-movements?${qs.toString()}`);
	return {
		items: (body?.data || []) as InventoryMovement[],
		total: (body?.meta?.total as number) || 0,
		page: (body?.meta?.page as number) || 1,
		page_size: (body?.meta?.page_size as number) || 20,
	};
}
