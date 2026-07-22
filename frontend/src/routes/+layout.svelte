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
		{ label: 'nav.customers', href: '/customers', icon: 'M16 11a4 4 0 1 0-8 0 4 4 0 0 0 8 0ZM4 20a8 8 0 0 1 16 0H4Z' },
		{ label: 'nav.suppliers', href: '/suppliers', icon: 'M3 20h18V9l-5 3V9l-5 3V4H3v16Zm4-4h3v2H7v-2Zm6 0h3v2h-3v-2Z' },
		{ label: 'nav.products', href: '/products', icon: 'M12 3 3.5 7.5 12 12l8.5-4.5L12 3Zm-8 7v7l8 4 8-4v-7l-8 4-8-4Z' },
		{ label: 'nav.categories', href: '/categories', icon: 'M4 5h7v6H4V5Zm9 0h7v6h-7V5ZM4 13h7v6H4v-6Zm9 0h7v6h-7v-6Z' },
		{ label: 'nav.tags', href: '/tags', icon: 'M4 5v6.5L12.5 20 20 12.5 11.5 4H5a1 1 0 0 0-1 1Zm4 4.5A1.5 1.5 0 1 1 8 6a1.5 1.5 0 0 1 0 3Z' },
		{ label: 'nav.purchases', href: '/purchases', icon: 'M5 4h2l1.2 10.5A2 2 0 0 0 10.2 16H18l2-8H8.7M10 20a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm7 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z' },
		{ label: 'nav.sales', href: '/sales', icon: 'M12 3v18m5-14H9.5a3 3 0 0 0 0 6H14a3 3 0 0 1 0 6H6' },
		{ label: 'nav.accounting', href: '/accounting', icon: 'M5 4h14v16H5V4Zm3 4h8M8 12h2m3 0h3M8 16h2m3 0h3' },
		{ label: 'nav.inventory', href: '/inventory', icon: 'M5 6h14v4H5V6Zm1 6h12v6H6v-6Zm4 2h4' },
		{ label: 'nav.reports', href: '/reports', icon: 'M5 19V9m7 10V5m7 14v-7' }
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
			aria-label="Close navigation"
			on:click={toggleSidebar}
		></button>
	{/if}

	<!-- Sidebar -->
	<aside
		class="app-sidebar fixed lg:static inset-y-0 {$dir === 'rtl' ? 'right-0' : 'left-0'} z-50 w-72 border-r transform transition-transform duration-200 ease-in-out
			{sidebarOpen ? 'translate-x-0' : ($dir === 'rtl' ? 'translate-x-full' : '-translate-x-full')}
			lg:translate-x-0 lg:relative overflow-y-auto"
	>
		<div class="p-5 border-b" style="border-color: var(--app-border);">
			<div class="flex items-center gap-3">
				<div class="grid h-11 w-11 place-items-center rounded-lg bg-teal-700 text-lg font-black text-white shadow-lg shadow-teal-900/20">
					TS
				</div>
				<div class="min-w-0">
					<h1 class="truncate text-xl font-black tracking-tight">{t('app.name')}</h1>
					<p class="text-xs font-semibold uppercase text-muted">Back office</p>
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

	<!-- Main content -->
	<div class="flex-1 flex flex-col min-w-0">
		<!-- Top bar -->
		<header class="app-topbar sticky top-0 z-30 flex items-center justify-between gap-4 border-b px-4 py-3 lg:px-6">
			<div class="flex min-w-0 items-center gap-3">
				<button
					on:click={toggleSidebar}
					class="btn lg:hidden !min-h-10 !w-10 !p-0"
					aria-label="Toggle sidebar"
				>
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
					</svg>
				</button>
				<div class="min-w-0">
					<p class="text-xs font-bold uppercase text-muted">{t('app.name')}</p>
					<h2 class="truncate text-lg font-black tracking-tight">{activeNav ? t(activeNav.label) : t('app.name')}</h2>
				</div>
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
						<button
							type="button"
							class="fixed inset-0 z-10"
							aria-label="Close user menu"
							on:click={() => { userMenuOpen = false; }}
						></button>
						<div class="card absolute {$dir === 'rtl' ? 'left-0' : 'right-0'} z-20 mt-2 w-56 overflow-hidden">
							<div class="border-b px-4 py-3" style="border-color: var(--app-border);">
								<p class="truncate text-sm font-bold">{$currentUser?.email || ''}</p>
								<p class="text-xs text-muted">Admin</p>
							</div>
							<button
								on:click={handleLogout}
								class="w-full px-4 py-3 text-start text-sm font-bold transition-colors hover:bg-rose-50 hover:text-rose-700"
							>
								{t('auth.logout')}
							</button>
						</div>
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
