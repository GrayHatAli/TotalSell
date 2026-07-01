import { apiRequest } from './client';

export interface TrialBalanceRow {
	account_id: number;
	code: string;
	name: string;
	debit: number;
	credit: number;
	balance: number;
}

export interface ProfitLossResult {
	total_revenue: number;
	total_expenses: number;
	net_profit: number;
	from_date: string;
	to_date: string;
}

export interface BalanceSheetResult {
	total_assets: number;
	total_liabilities: number;
	total_equity: number;
	liabilities_plus_equity: number;
	is_balanced: boolean;
	as_of_date: string;
}

export interface SalesReport {
	total_revenue: number;
	invoice_count: number;
	from_date: string;
	to_date: string;
	by_customer: { customer_id: number; name: string; total: number; count: number }[];
	by_product: { product_id: number; name: string; total: number; quantity: number }[];
}

export interface PurchaseReport {
	total_purchases: number;
	invoice_count: number;
	from_date: string;
	to_date: string;
	by_supplier: { supplier_id: number; name: string; total: number; count: number }[];
}

export interface InventoryReport {
	items: {
		product_id: number;
		name: string;
		sku: string;
		category: string | null;
		stock: number;
		min_stock: number;
		cost_price: number;
		sale_price: number;
		low_stock: boolean;
	}[];
	low_stock_count: number;
}

export async function getTrialBalance(date?: string): Promise<TrialBalanceRow[]> {
	const qs = date ? `?date=${encodeURIComponent(date)}` : '';
	const body = await apiRequest<any>(`/accounting/trial-balance${qs}`);
	return (body?.data || []) as TrialBalanceRow[];
}

export async function getProfitLoss(fromDate: string, toDate: string): Promise<ProfitLossResult> {
	const qs = `?from_date=${encodeURIComponent(fromDate)}&to_date=${encodeURIComponent(toDate)}`;
	const body = await apiRequest<any>(`/accounting/profit-loss${qs}`);
	if (!body?.data) throw new Error('Failed to fetch profit/loss');
	return body.data;
}

export async function getBalanceSheet(date?: string): Promise<BalanceSheetResult> {
	const qs = date ? `?date=${encodeURIComponent(date)}` : '';
	const body = await apiRequest<any>(`/accounting/balance-sheet${qs}`);
	if (!body?.data) throw new Error('Failed to fetch balance sheet');
	return body.data;
}

export async function getSalesReport(fromDate: string, toDate: string): Promise<SalesReport> {
	const qs = `?from_date=${encodeURIComponent(fromDate)}&to_date=${encodeURIComponent(toDate)}`;
	const body = await apiRequest<any>(`/reports/sales${qs}`);
	if (!body?.data) throw new Error('Failed to fetch sales report');
	return body.data;
}

export async function getPurchaseReport(fromDate: string, toDate: string): Promise<PurchaseReport> {
	const qs = `?from_date=${encodeURIComponent(fromDate)}&to_date=${encodeURIComponent(toDate)}`;
	const body = await apiRequest<any>(`/reports/purchases${qs}`);
	if (!body?.data) throw new Error('Failed to fetch purchases report');
	return body.data;
}

export async function getInventoryReport(): Promise<InventoryReport> {
	const body = await apiRequest<any>('/reports/inventory');
	if (!body?.data) throw new Error('Failed to fetch inventory report');
	return body.data;
}

export function downloadPdf(url: string): void {
	const a = document.createElement('a');
	a.href = url;
	a.download = url.split('/').pop() || 'report.pdf';
	a.click();
}

export function downloadExcel(url: string): void {
	const a = document.createElement('a');
	a.href = url;
	a.download = url.split('/').pop() || 'report.xlsx';
	a.click();
}
