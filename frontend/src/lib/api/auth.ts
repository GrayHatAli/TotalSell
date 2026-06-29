import { apiRequest, type TokenPair } from './client';

export interface UserResponse {
	id: number;
	email: string;
	is_active: boolean;
	is_admin: boolean;
}

export async function loginRequest(email: string, password: string): Promise<TokenPair> {
	const body = await apiRequest<TokenPair>('/auth/login', {
		method: 'POST',
		body: JSON.stringify({ email, password })
	});
	if (!body.data) throw new Error('Login failed: no data returned');
	return body.data;
}

export async function logoutRequest(refreshToken: string): Promise<void> {
	await apiRequest('/auth/logout', {
		method: 'POST',
		body: JSON.stringify({ refresh_token: refreshToken })
	});
}

export async function fetchMe(): Promise<UserResponse> {
	const body = await apiRequest<UserResponse>('/auth/me');
	if (!body.data) throw new Error('Failed to fetch user');
	return body.data;
}
