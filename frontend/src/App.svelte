<script>
	import * as Api from './Api'
		
	let osReleasePromise = Api.osRelase()


</script>

<main>
	<h1>Next Linux</h1>
	{#await osReleasePromise}
		<p>Loading os version...</p>
	{:then osRelease} 
		<p>Your linux version is {osRelease}</p>
	{/await}	
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>