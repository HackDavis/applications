<template>
<div class="container">
	<div class="columns">

		<!-- Control panel -->
		<div class="column has-background-light is-3">		
			<center>
				<!-- Person's Image -->
				<figure class="image is-128x128">
					<img class="profile-picture" alt="" src="https://bulma.io/images/placeholders/256x256.png">
				</figure>

				<!-- Person's name -->			
				<div class="subtitle is-4" style="margin: 16px;">Full-name</div>

				<!-- Break for looking good :D -->
				<div class="pad-light"></div>
				<div class="break"></div>
				<div class="pad-light"></div>

				<!-- Rating control -->
				<div class="subtitle is-4" style="margin: 16px;">Rating</div>
				<div class="buttons has-addons is-centered">
					<span class="button">1</span>
					<span class="button">2</span>
					<span class="button">3</span>
					<span class="button">4</span>
					<span class="button">5</span>
				</div>

				<!-- Next applicant button -->
				<a class="button is-primary is-medium">Next applicant</a>
				<div class="pad"></div>			
			</center>		
		</div>

		<!-- Information panel -->
		<div class="column has-background-light">

			<!-- Major -->
			<div class="title" style="margin: 16px;">Major</div>	
			<div class="subtitle is-4" style="margin: 16px;">{{major}}</div>
			<div class="pad-light"></div>		

			<!-- Year -->
			<div class="title" style="margin: 16px;">College year</div>	
			<div class="subtitle is-4" style="margin: 16px;">{{year}}</div>	
			<div class="pad-light"></div>	

			<!-- Essays -->
			<div class="title" style="margin: 16px;">Text information</div>	
			<div class="subtitle is-4" style="margin: 16px;">REPLACE ME</div>	
			<div class="pad"></div>		

			<!-- Resume -->
			<div class="title" style="margin: 16px;">Resume</div>			
			<div>
				<a class="button is-primary is-medium" style="margin-left: 16px;">Resume</a>					
			</div>			
			<iframe src="http://josharnoldjosh.github.io" width="80%" height="250px" style="overflow:auto; margin-top: 16px;"></iframe>
			<div class="pad"></div>

			<!-- Github -->
			<div class="title" style="margin: 16px;">Github</div>	
			<a class="button is-primary is-medium" style="margin-left: 16px;">Github</a>
			<div class="pad"></div>	

			<!-- LinkedIn -->
			<div class="title" style="margin: 16px;">LinkedIn</div>	
			<a class="button is-primary is-medium" style="margin-left: 16px;">LinkedIn</a>
			<div class="pad"></div>													
		</div>
	</div>
</div>
</template>

<script>  
export default {

}
</script>


