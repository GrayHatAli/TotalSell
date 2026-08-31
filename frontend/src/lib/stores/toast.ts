import { writable } from 'svelte/store';

export interface Toast {
	id: string;
	message: string;
	title?: string;
	type?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
	duration?: number;
}

// Store holds an array of toasts
const toastStore = writable<Toast[]>([]);

// Extract store methods
const { subscribe, set, update } = toastStore;

export const toast = {
	subscribe,
	show: (options: Omit<Toast, 'id'>) => {
		const toastItem: Toast = {
			id: Math.random().toString(36).substr(2, 9),
			...options,
		};
		update((items) => [toastItem, ...items]);
	},
	success: (message: string, title?: string) => {
		toast.show({ message, title, type: 'success' });
	},
	error: (message: string, title?: string) => {
		toast.show({ message, title, type: 'error' });
	},
	warning: (message: string, title?: string) => {
		toast.show({ message, title, type: 'warning' });
	},
	info: (message: string, title?: string) => {
		toast.show({ message, title, type: 'info' });
	},
	dismiss: (id: string) => {
		update((items) => items.filter((t) => t.id !== id));
	},
	dismissAll: () => {
		set([]);
	},
};
