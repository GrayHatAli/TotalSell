import { apiRequest } from '$lib/api/client';

export interface Account {
	id: number;
	code: string;
	name: string;
	account_type: string;
	parent_id?: number;
	is_active: boolean;
}

export async function listAccounts(): Promise<Account[]> {
	const body = await apiRequest<any>('/accounts');
	return (body?.data || []) as Account[];
}
