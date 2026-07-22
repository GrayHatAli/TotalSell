import { writable, derived } from 'svelte/store';
import en from './en.json';
import fa from './fa.json';

export type Locale = 'en' | 'fa';

const translations: Record<Locale, Record<string, string>> = { en, fa };

export const locale = writable<Locale>('en');
export const dir = derived(locale, ($locale) => ($locale === 'fa' ? 'rtl' : 'ltr'));

let currentLocale: Locale = 'en';
locale.subscribe((l) => (currentLocale = l));

export function t(key: string): string {
	return translations[currentLocale]?.[key] ?? translations['en']?.[key] ?? key;
}

export function setLocale(l: Locale): void {
	locale.set(l);
	if (typeof document !== 'undefined') {
		document.documentElement.lang = l;
		document.documentElement.dir = l === 'fa' ? 'rtl' : 'ltr';
	}
}
