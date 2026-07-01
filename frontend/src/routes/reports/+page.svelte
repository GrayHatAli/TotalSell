<script lang="ts">
	import { t } from '$lib/i18n';
</script>

<div class="max-w-5xl mx-auto space-y-6">
	<h1 class="text-2xl font-bold">Reports</h1>
	<div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
		<a href="/reports/trial-balance" class="card p-6 hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors">
			<h2 class="text-lg font-semibold">Trial Balance</h2>
			<p class="text-sm text-gray-500 dark:text-gray-400 mt-2">Account balances as of a date</p>
		</a>
		<a href="/reports/profit-loss" class="card p-6 hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors">
			<h2 class="text-lg font-semibold">Profit & Loss</h2>
			<p class="text-sm text-gray-500 dark:text-gray-400 mt-2">Revenue, expenses, and net profit</p>
		</a>
		<a href="/reports/balance-sheet" class="card p-6 hover:bg-surface-200 dark:hover:bg-surface-700 transition-colors">
			<h2 class="text-lg font-semibold">Balance Sheet</h2>
			<p class="text-sm text-gray-500 dark:text-gray-400 mt-2">Assets, liabilities, and equity</p>
		</a>
	</div>
</div>
