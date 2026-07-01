import { apiRequest } from '$lib/api/client';

export interface BankAccount {
	id: number;
	name: string;
	account_type: string;
	iban?: string;
	account_number?: string;
	bank_name?: string;
	opening_balance: number;
	current_balance: number;
	active: boolean;
	notes?: string;
	created_at: string;
	updated_at: string;
}

export async function listBankAccounts(): Promise<BankAccount[]> {
	const body = await apiRequest<any>('/bank-accounts');
	return (body?.data || []) as BankAccount[];
}

export async function createBankAccount(data: Partial<BankAccount>): Promise<BankAccount> {
	const body = await apiRequest<any>('/bank-accounts', {
		method: 'POST',
		body: JSON.stringify(data),
	});
	if (!body?.data) throw new Error('Failed to create bank account');
	return body.data as BankAccount;
}

export async function updateBankAccount(id: number, data: Partial<BankAccount>): Promise<BankAccount> {
	const body = await apiRequest<any>(`/bank-accounts/${id}`, {
		method: 'PATCH',
		body: JSON.stringify(data),
	});
	if (!body?.data) throw new Error('Failed to update bank account');
	return body.data as BankAccount;
}

export async function deleteBankAccount(id: number): Promise<void> {
	await apiRequest(`/bank-accounts/${id}`, { method: 'DELETE' });
}
