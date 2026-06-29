import { writable } from 'svelte/store';
import type { UserResponse } from '$lib/api/auth';
import { getAccessToken } from '$lib/api/client';

export const currentUser = writable<UserResponse | null>(null);
export const isAuthenticated = writable<boolean>(!!getAccessToken());
