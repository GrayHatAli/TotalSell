const API_BASE = import.meta.env.PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export interface ErrorInfo {
	code: string;
	message: string;
	details: Record<string, unknown> | null;
}

export interface ApiResponse<T = unknown> {
	success: boolean;
	data: T | null;
	meta: Record<string, unknown> | null;
	error: ErrorInfo | null;
}

export interface TokenPair {
	access_token: string;
	refresh_token: string;
	token_type: string;
}

function getAccessToken(): string | null {
	if (typeof window === 'undefined') return null;
	return localStorage.getItem('access_token');
}

function getRefreshToken(): string | null {
	if (typeof window === 'undefined') return null;
	return localStorage.getItem('refresh_token');
}

function setTokens(pair: TokenPair): void {
	localStorage.setItem('access_token', pair.access_token);
	localStorage.setItem('refresh_token', pair.refresh_token);
}

function clearTokens(): void {
	localStorage.removeItem('access_token');
	localStorage.removeItem('refresh_token');
}

async function refreshAccessToken(): Promise<string | null> {
	const refresh = getRefreshToken();
	if (!refresh) return null;

	try {
		const res = await fetch(`${API_BASE}/auth/refresh`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ refresh_token: refresh })
		});
		if (!res.ok) {
			clearTokens();
			return null;
		}
		const body: ApiResponse<TokenPair> = await res.json();
		if (body.success && body.data) {
			setTokens(body.data);
			return body.data.access_token;
		}
		clearTokens();
		return null;
	} catch {
		clearTokens();
		return null;
	}
}

export interface ListResponse<T> {
	items: T[];
	total: number;
	page: number;
	page_size: number;
}

/**
 * Normalize a backend list response. Backend list endpoints return
 * `{ success, data: [...], meta: { page, page_size, total } }`.
 */
export function normalizeList<T>(body: ApiResponse<T[]>): ListResponse<T> {
	if (!body.success || !body.data) {
		throw new Error(body.error?.message || 'Request failed');
	}
	return {
		items: body.data,
		total: (body.meta?.total as number) ?? body.data.length,
		page: (body.meta?.page as number) ?? 1,
		page_size: (body.meta?.page_size as number) ?? body.data.length
	};
}

export async function apiRequest<T>(
	endpoint: string,
	options: RequestInit = {}
): Promise<ApiResponse<T>> {
	const token = getAccessToken();
	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		...((options.headers as Record<string, string>) || {})
	};

	if (token) {
		headers['Authorization'] = `Bearer ${token}`;
	}

	let res = await fetch(`${API_BASE}${endpoint}`, {
		...options,
		headers
	});

	// If 401, try refreshing the token
	if (res.status === 401 && getRefreshToken()) {
		const newToken = await refreshAccessToken();
		if (newToken) {
			headers['Authorization'] = `Bearer ${newToken}`;
			res = await fetch(`${API_BASE}${endpoint}`, {
				...options,
				headers
			});
		}
	}

	const body: ApiResponse<T> = await res.json();

	if (!res.ok && !body.success) {
		throw new Error(body.error?.message || `Request failed with status ${res.status}`);
	}

	if (!res.ok) {
		throw new Error(`Request failed with status ${res.status}`);
	}

	return body;
}

export async function apiLogin(accessToken: string, refreshToken: string): Promise<void> {
	localStorage.setItem('access_token', accessToken);
	localStorage.setItem('refresh_token', refreshToken);
}

export function apiLogout(): void {
	clearTokens();
}

export function isAuthenticated(): boolean {
	return !!getAccessToken();
}

export { getAccessToken, getRefreshToken, setTokens, clearTokens, refreshAccessToken };
