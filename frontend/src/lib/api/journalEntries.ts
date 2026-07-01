import { apiRequest } from './client';

export interface JournalEntry {
	id: number;
	date: string;
	description?: string;
	reference_type?: string;
	reference_id?: number;
	lines?: JournalLine[];
}

export interface JournalLine {
	account_id: number;
	debit: number;
	credit: number;
	note?: string;
}

export async function listJournalEntries(params: Record<string, string | number | undefined>): Promise<{ items: JournalEntry[]; total: number; page: number; page_size: number }> {
	const qs = new URLSearchParams();
	Object.entries(params).forEach(([k, v]) => { if (v !== undefined && v !== '') qs.set(k, String(v)); });
	const body = await apiRequest<any>(`/accounting/journal-entries?${qs.toString()}`);
	return {
		items: (body?.data || []) as JournalEntry[],
		total: (body?.meta?.total as number) || 0,
		page: (body?.meta?.page as number) || 1,
		page_size: (body?.meta?.page_size as number) || 20,
	};
}

export async function createJournalEntry(payload: { date: string; description?: string; lines: JournalLine[] }): Promise<{ id: number }> {
	const body = await apiRequest<any>('/accounting/journal-entries', { method: 'POST', body: JSON.stringify(payload) });
	if (!body?.data) throw new Error('Failed to create journal entry');
	return body.data;
}
