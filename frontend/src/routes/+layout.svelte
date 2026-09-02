<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { currentUser, isAuthenticated } from '$lib/stores/auth';
	import { locale, dir, setLocale, t } from '$lib/i18n';
	import { fetchMe, logoutRequest } from '$lib/api/auth';
	import { apiLogout, getRefreshToken } from '$lib/api/client';
	import { browser } from '$app/environment';
	import ToastContainer from '$lib/components/ToastContainer.svelte';

	let sidebarOpen = false;
	let userMenuOpen = false;
	$: isLoginPage = $page.url.pathname === '/login';
	$: activeNav = navItems.find((item) => $page.url.pathname.startsWith(item.href));

	$: {
		if (typeof document !== 'undefined') {
			document.documentElement.dir = $dir;
			document.documentElement.lang = $locale;
		}
	}

	onMount(async () => {
		const saved = localStorage.getItem('locale') as 'en' | 'fa' | null;
		if (saved) {
			setLocale(saved);
		}

		if ($isAuthenticated) {
			try {
				const user = await fetchMe();
				$currentUser = user;
			} catch {
				$isAuthenticated = false;
				if ($page.url.pathname !== '/login') {
					goto('/login');
				}
			}
		}
	});

	$: if (browser && !$isAuthenticated && $page.url.pathname !== '/login') {
		goto('/login');
	}

	function toggleSidebar() {
		sidebarOpen = !sidebarOpen;
	}

	async function handleLogout() {
		const refreshToken = getRefreshToken();
		if (refreshToken) {
			try {
				await logoutRequest(refreshToken);
			} catch {
				// ignore
			}
		}
		apiLogout();
		$currentUser = null;
		$isAuthenticated = false;
		userMenuOpen = false;
		goto('/login');
	}

	function switchLocale() {
		const next = $locale === 'en' ? 'fa' : 'en';
		setLocale(next);
		localStorage.setItem('locale', next);
	}

	const navItems = [
		{ label: 'nav.dashboard', href: '/dashboard', icon: 'M4 13h6V4H4v9Zm10 7h6V4h-6v16ZM4 20h6v-5H4v5Z' },
		{ label: 'nav.sales', href: '/sales', icon: 'M3 3v18h18M8 16v-5m4 5V8m4 8v-3' },
		{ label: 'nav.purchases', href: '/purchases', icon: 'M6 7V6a6 6 0 1 1 12 0v1h2.2l1 14H2.8l1-14H6Zm2 0h8V6a4 4 0 0 0-8 0v1Z' },
		{ label: 'nav.payments', href: '/payments', icon: 'M2 7a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V7Zm0 3h20' },
		{ label: 'nav.customers', href: '/customers', icon: 'M16 11a4 4 0 1 0-8 0 4 4 0 0 0 8 0ZM4 20a8 8 0 0 1 16 0H4Z' },
		{ label: 'nav.suppliers', href: '/suppliers', icon: 'M3 20h18V9l-5 3V9l-5 3V4H3v16Zm4-4h3v2H7v-2Zm6 0h3v2h-3v-2Z' },
		{ label: 'nav.products', href: '/products', icon: 'M12 3 3.5 7.5 12 12l8.5-4.5L12 3Zm-8 7v7l8 4 8-4v-7l-8 4-8-4Z' },
		{ label: 'nav.categories', href: '/categories', icon: 'M4 5h7v6H4V5Zm9 0h7v6h-7V5ZM4 13h7v6H4v-6Zm9 0h7v6h-7v-6Z' },
		{ label: 'nav.tags', href: '/tags', icon: 'M4 5v6.5L12.5 20 20 12.5 11.5 4H5' },
		{ label: 'nav.inventory', href: '/inventory', icon: 'M16.5 9.4 7.55 4.24M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z' },
		{ label: 'nav.bankAccounts', href: '/bank-accounts', icon: 'M3 10l9-6 9 6M5 10v8m4-8v8m6-8v8m4-8v8M3 20h18' },
		{ label: 'nav.accounting', href: '/accounting/journal-entries', icon: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 1 6.5 22H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15Z' },
		{ label: 'nav.reports', href: '/reports', icon: 'M3 3v18h18M7 15l4-4 3 3 5-6' }
	];
</script>

{#if isLoginPage}
	<slot />
{:else}
<div class="app-shell flex h-screen overflow-hidden {$dir === 'rtl' ? 'flex-row-reverse' : ''}">
	<!-- Mobile overlay -->
	{#if sidebarOpen}
		<button
			type="button"
			class="fixed inset-0 z-40 bg-black/50 lg:hidden"
			aria-label={t('common.closeNav')}
			on:click={toggleSidebar}
		></button>
	{/if}

	<!-- Sidebar -->
	{#key $locale}
	<aside
		class="app-sidebar fixed lg:static inset-y-0 {$dir === 'rtl' ? 'right-0' : 'left-0'} z-50 w-72 border-e transform transition-transform duration-200 ease-in-out
			{sidebarOpen ? 'translate-x-0' : ($dir === 'rtl' ? 'translate-x-full' : '-translate-x-full')}
			lg:translate-x-0 lg:relative overflow-y-auto"
	>
		<div class="p-5 border-b" style="border-color: var(--app-border);">
			<div class="flex items-center gap-3">
				<div class="grid h-11 w-11 place-items-center rounded-xl bg-emerald-600 text-lg font-black text-white shadow-sm">T</div>
				<div>
					<p class="text-base font-black tracking-tight">{t('app.name')}</p>
					<p class="text-[11px] font-semibold uppercase tracking-wider text-muted">{t('app.tagline')}</p>
				</div>
			</div>
		</div>

		<nav class="p-3 space-y-1.5">
			{#each navItems as item}
				<a
					href={item.href}
					class="nav-link {$page.url.pathname.startsWith(item.href) ? 'nav-link-active' : ''}"
					on:click={() => { sidebarOpen = false; }}
				>
					<span class="nav-icon" aria-hidden="true">
						<svg class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" d={item.icon} />
						</svg>
					</span>
					<span>{t(item.label)}</span>
				</a>
			{/each}
		</nav>

		<div class="sticky bottom-0 mt-4 border-t p-4 backdrop-blur" style="border-color: var(--app-border); background: color-mix(in srgb, var(--app-panel) 88%, transparent);">
			<button
				on:click={switchLocale}
				class="btn w-full justify-start"
			>
				<span class="grid h-7 w-7 place-items-center rounded-md bg-amber-100 text-xs font-black text-amber-800">{$locale === 'en' ? 'فا' : 'EN'}</span>
				<span>{$locale === 'en' ? 'فارسی' : 'English'}</span>
			</button>
		</div>
	</aside>
	{/key}

	<!-- Main content -->
	<div class="flex-1 flex flex-col min-w-0">
		<!-- Top bar -->
		<header class="app-topbar sticky top-0 z-30 flex items-center justify-between gap-4 border-b px-4 py-3 lg:px-6">
			<div class="flex min-w-0 items-center gap-3">
				<button
					on:click={toggleSidebar}
					class="btn btn-ghost lg:hidden !min-h-10 !w-10 !p-0"
					aria-label={t('common.toggleNav')}
				>
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
					</svg>
				</button>
				{#key $locale}
					<div class="min-w-0">
						<p class="truncate text-base font-bold tracking-tight">{activeNav ? t(activeNav.label) : t('app.name')}</p>
						<p class="text-[11px] font-semibold uppercase tracking-wider text-muted">{t('app.name')}</p>
					</div>
				{/key}
			</div>

			{#if $isAuthenticated}
				<div class="relative flex items-center gap-2">
					<button
						on:click={() => { userMenuOpen = !userMenuOpen; }}
						class="btn"
					>
						<div class="flex h-8 w-8 items-center justify-center rounded-md bg-teal-700 text-sm font-black text-white">
							{$currentUser?.email?.charAt(0).toUpperCase() || 'A'}
						</div>
						<span class="hidden max-w-48 truncate text-sm sm:block">{$currentUser?.email || ''}</span>
					</button>

					{#if userMenuOpen}
						{#key $locale}
						<button
							type="button"
							class="fixed inset-0 z-10"
							aria-label={t('common.closeMenu')}
							on:click={() => { userMenuOpen = false; }}
						></button>
						<div class="card absolute {$dir === 'rtl' ? 'left-0' : 'right-0'} z-20 mt-2 w-56 overflow-hidden">
							<div class="border-b px-4 py-3" style="border-color: var(--app-border);">
								<p class="truncate text-sm font-bold">{$currentUser?.email || ''}</p>
								<p class="text-xs text-muted">{t('auth.adminRole')}</p>
							</div>
							<button
								on:click={handleLogout}
								class="w-full px-4 py-3 text-start text-sm font-bold transition-colors hover:bg-rose-50 hover:text-rose-700 dark:hover:bg-rose-950/40"
							>
								{t('auth.logout')}
							</button>
						</div>
						{/key}
					{/if}
				</div>
			{/if}
		</header>

		<!-- Page content -->
		<main class="app-main flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8">
			{#key $locale}
				<slot />
			{/key}
		</main>
	</div>
</div>
{/if}

<ToastContainer />
