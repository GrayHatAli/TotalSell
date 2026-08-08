import { writable } from 'svelte/store';

interface Toast {
	id: string;
	message: string;
	title?: string;
	type?: 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error';
	duration?: number;
}

const toastStore = writable<Toast[]>([]);

interface ToastActions {
	show: (options: Omit<Toast, 'id'>) => void;
	success: (message: string, title?: string) => void;
	error: (message: string, title?: string) => void;
	warning: (message: string, title?: string) => void;
	info: (message: string, title?: string) => void;
	dismiss: (id: string) => void;
	dismissAll: () => void;
}

const { subscribe, set, update }: any = writable<Toast[]>([]);

const toast = {
	subscribe,
	show: (options: Omit<Toast, 'id'>) => {
		const toast: Toast = {
			id: Math.random().toString(36).substr(2, 9),
			...options,
		};
		update((items) => [toast, ...items]);
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

export default toast;