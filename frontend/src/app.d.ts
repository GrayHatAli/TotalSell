/// <reference types="@sveltejs/kit" />

declare namespace App {
	interface Locals {
		locale: string;
		dir: 'ltr' | 'rtl';
	}
}
