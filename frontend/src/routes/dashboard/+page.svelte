<script lang="ts">
	import { currentUser } from '$lib/stores/auth';
	import { t } from '$lib/i18n';
</script>

<div class="max-w-4xl mx-auto space-y-6">
	<div class="card p-6">
		<h1 class="text-2xl font-bold">{t('dashboard.welcome')}</h1>
		<p class="mt-2 text-surface-600 dark:text-surface-400">
			{$currentUser?.email ? `Logged in as ${$currentUser.email}` : ''}
		</p>
		<p class="mt-1 text-surface-500 dark:text-surface-500">
			{t('dashboard.description')}
		</p>
	</div>

	<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
		<div class="card p-4 hover:shadow-lg transition-shadow">
			<h3 class="font-semibold text-lg">{t('nav.customers')}</h3>
			<p class="text-surface-500 dark:text-surface-400 text-sm mt-1">0 customers</p>
		</div>
		<div class="card p-4 hover:shadow-lg transition-shadow">
			<h3 class="font-semibold text-lg">{t('nav.products')}</h3>
			<p class="text-surface-500 dark:text-surface-400 text-sm mt-1">0 products</p>
		</div>
		<div class="card p-4 hover:shadow-lg transition-shadow">
			<h3 class="font-semibold text-lg">{t('nav.sales')}</h3>
			<p class="text-surface-500 dark:text-surface-400 text-sm mt-1">0 invoices</p>
		</div>
	</div>
</div>
