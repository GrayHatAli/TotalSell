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
