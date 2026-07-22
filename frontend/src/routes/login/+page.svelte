<script lang="ts">
	import { goto } from '$app/navigation';
	import { currentUser, isAuthenticated } from '$lib/stores/auth';
	import { loginRequest } from '$lib/api/auth';
	import { apiLogin } from '$lib/api/client';
	import { locale, setLocale, t } from '$lib/i18n';
	import { onMount } from 'svelte';

	let email = '';
	let password = '';
	let error = '';
	let loading = false;

	// If already authenticated, redirect to dashboard
	onMount(() => {
		if ($isAuthenticated) {
			goto('/dashboard');
		}
	});

	async function handleSubmit() {
		error = '';
		if (!email || !password) {
			error = 'Please enter email and password';
			return;
		}

		loading = true;
		try {
			const tokenPair = await loginRequest(email, password);
			apiLogin(tokenPair.access_token, tokenPair.refresh_token);
			$isAuthenticated = true;
			goto('/dashboard');
		} catch (e: unknown) {
			error = e instanceof Error ? e.message : t('auth.invalidCredentials');
		} finally {
			loading = false;
		}
	}
</script>

{#key $locale}
<div class="min-h-screen flex items-center justify-center bg-surface-100 dark:bg-surface-900 px-4">
	<div class="w-full max-w-sm">
		<div class="text-center mb-8">
			<h1 class="text-3xl font-bold text-primary-500">{t('app.name')}</h1>
			<p class="mt-2 text-surface-600 dark:text-surface-400">{t('auth.loginSubtitle')}</p>
		</div>

		<div class="card p-6 space-y-6">
			<h2 class="text-xl font-semibold text-center">{t('auth.loginTitle')}</h2>

			<form on:submit|preventDefault={handleSubmit} class="space-y-4">
				<div class="space-y-1">
					<label for="email" class="text-sm font-medium">{t('auth.email')}</label>
					<input
						id="email"
						type="email"
						bind:value={email}
						class="input w-full"
						placeholder="admin@example.com"
						autocomplete="email"
						required
					/>
				</div>

				<div class="space-y-1">
					<label for="password" class="text-sm font-medium">{t('auth.password')}</label>
					<input
						id="password"
						type="password"
						bind:value={password}
						class="input w-full"
						placeholder="••••••••"
						autocomplete="current-password"
						required
					/>
				</div>

				{#if error}
					<div class="p-3 bg-error-100 dark:bg-error-900/30 border border-error-300 dark:border-error-700 text-error-700 dark:text-error-300 rounded-lg text-sm">
						{error}
					</div>
				{/if}

				<button
					type="submit"
					class="btn btn-primary w-full"
					disabled={loading}
				>
					{#if loading}
						<span class="loading-ring mr-2"></span>
					{/if}
					{t('auth.login')}
				</button>
			</form>
		</div>
	</div>
</div>
{/key}