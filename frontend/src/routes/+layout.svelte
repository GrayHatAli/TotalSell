<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import type { Workbox } from 'workbox-window';

	onMount(() => {
		if ('serviceWorker' in navigator) {
			import('virtual:pwa-register').then(({ registerSW }) => {
				registerSW({
					immediate: true,
					onNeedRefresh() {
						if (confirm('New version available. Reload?')) {
							location.reload();
						}
					}
				});
			});
		}
	});
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { currentUser, isAuthenticated } from '$lib/stores/auth';
	import { locale, dir, setLocale, t } from '$lib/i18n';
	import { fetchMe, logoutRequest } from '$lib/api/auth';
	import { apiLogout, getRefreshToken } from '$lib/api/client';

	let sidebarOpen = false;
	let userMenuOpen = false;
	let currentLocale: 'en' | 'fa' = 'en';

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
			currentLocale = saved;
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

	$: if (!$isAuthenticated && $page.url.pathname !== '/login') {
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
		const next = currentLocale === 'en' ? 'fa' : 'en';
		currentLocale = next;
		setLocale(next);
		localStorage.setItem('locale', next);
	}

	const navItems = [
		{ label: 'nav.dashboard', href: '/dashboard', icon: '📊' },
		{ label: 'nav.customers', href: '/customers', icon: '👥' },
		{ label: 'nav.suppliers', href: '/suppliers', icon: '🏭' },
		{ label: 'nav.products', href: '/products', icon: '📦' },
		{ label: 'nav.categories', href: '/categories', icon: '📁' },
		{ label: 'nav.tags', href: '/tags', icon: '🔖' },
		{ label: 'nav.purchases', href: '/purchases', icon: '🛒' },
		{ label: 'nav.sales', href: '/sales', icon: '💰' },
		{ label: 'nav.accounting', href: '/accounting', icon: '📒' },
		{ label: 'nav.inventory', href: '/inventory', icon: '📋' },
		{ label: 'nav.reports', href: '/reports', icon: '📈' }
	];
</script>

<div class="flex h-screen overflow-hidden {$dir === 'rtl' ? 'flex-row-reverse' : ''}">
	<!-- Mobile overlay -->
	{#if sidebarOpen}
		<!-- svelte-ignore a11y_click_events_have_key_events -->
		<!-- svelte-ignore a11y_no_static_element_interactions -->
		<div
			class="fixed inset-0 bg-black/50 z-40 lg:hidden"
			on:click={toggleSidebar}
		></div>
	{/if}

	<!-- Sidebar -->
	<aside
		class="fixed lg:static inset-y-0 {$dir === 'rtl' ? 'right-0' : 'left-0'} z-50 w-64 bg-surface-200 dark:bg-surface-800 transform transition-transform duration-200 ease-in-out
			{sidebarOpen ? 'translate-x-0' : ($dir === 'rtl' ? 'translate-x-full' : '-translate-x-full')}
			lg:translate-x-0 lg:relative overflow-y-auto"
	>
		<div class="p-4 border-b border-surface-300 dark:border-surface-700">
			<h1 class="text-xl font-bold">{t('app.name')}</h1>
		</div>

		<nav class="p-2 space-y-1">
			{#each navItems as item}
				<a
					href={item.href}
					class="flex items-center gap-3 px-3 py-2 rounded-lg transition-colors
						{$page.url.pathname.startsWith(item.href)
							? 'bg-primary-500 text-white'
							: 'hover:bg-surface-300 dark:hover:bg-surface-700'}"
					on:click={() => { sidebarOpen = false; }}
				>
					<span class="text-lg">{item.icon}</span>
					<span>{t(item.label)}</span>
				</a>
			{/each}
		</nav>

		<div class="absolute bottom-0 left-0 right-0 p-4 border-t border-surface-300 dark:border-surface-700 bg-surface-200 dark:bg-surface-800">
			<button
				on:click={switchLocale}
				class="w-full flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-surface-300 dark:hover:bg-surface-700 transition-colors text-sm"
			>
				<span class="text-lg">{currentLocale === 'en' ? '🇮🇷' : '🇬🇧'}</span>
				<span>{currentLocale === 'en' ? 'فارسی' : 'English'}</span>
			</button>
		</div>
	</aside>

	<!-- Main content -->
	<div class="flex-1 flex flex-col min-w-0">
		<!-- Top bar -->
		<header class="flex items-center justify-between px-4 py-3 border-b border-surface-300 dark:border-surface-700 bg-surface-100 dark:bg-surface-900">
			<div class="flex items-center gap-2">
				<button
					on:click={toggleSidebar}
					class="lg:hidden p-2 rounded-lg hover:bg-surface-300 dark:hover:bg-surface-700 transition-colors"
					aria-label="Toggle sidebar"
				>
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
					</svg>
				</button>
				<h2 class="text-lg font-semibold">{t('app.name')}</h2>
			</div>

			{#if $isAuthenticated}
				<div class="relative">
					<button
						on:click={() => { userMenuOpen = !userMenuOpen; }}
						class="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-surface-300 dark:hover:bg-surface-700 transition-colors"
					>
						<div class="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center text-white text-sm font-medium">
							{$currentUser?.email?.charAt(0).toUpperCase() || 'A'}
						</div>
						<span class="hidden sm:block text-sm">{$currentUser?.email || ''}</span>
					</button>

					{#if userMenuOpen}
						<!-- svelte-ignore a11y_click_events_have_key_events -->
						<!-- svelte-ignore a11y_no_static_element_interactions -->
						<div
							class="fixed inset-0 z-10"
							on:click={() => { userMenuOpen = false; }}
						></div>
						<div class="absolute {$dir === 'rtl' ? 'left-0' : 'right-0'} mt-2 w-48 bg-surface-200 dark:bg-surface-800 rounded-lg shadow-xl border border-surface-300 dark:border-surface-700 z-20">
							<div class="px-4 py-3 border-b border-surface-300 dark:border-surface-700">
								<p class="text-sm font-medium truncate">{$currentUser?.email || ''}</p>
							</div>
							<button
								on:click={handleLogout}
								class="w-full text-left px-4 py-2 text-sm hover:bg-surface-300 dark:hover:bg-surface-700 transition-colors"
							>
								{t('auth.logout')}
							</button>
						</div>
					{/if}
				</div>
			{/if}
		</header>

		<!-- Page content -->
		<main class="flex-1 overflow-y-auto p-4">
			<slot />
		</main>
	</div>
</div>
