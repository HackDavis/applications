<template>
<div class="container">
	<div class="columns">

		<!-- Control panel -->
		<div class="column section-column has-background-white is-3">		
			<center>
	

				<!-- Person's name -->			
				<div class="subtitle is-4" style="margin: 1em;">Full-name</div>

				<!-- Break for looking good :D -->								
				<div class="pad-light"></div>

				<!-- Rating control -->
				<div class="subtitle is-4" style="margin: 1em;">Rating</div>

				<div class="control-group columns">

				<label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >1
				<input type="radio" name="radio" checked="checked"/>
				<div class="control__indicator"></div>
				</label>

				<label class="control control--radio column is-flex is-align-center is-flex-column-reverse">2
				<input type="radio" name="radio" checked="checked"/>
				<div class="control__indicator"></div>
				</label>	

				<label class="control control--radio column is-flex is-align-center is-flex-column-reverse" >3
				<input type="radio" name="radio" checked="checked"/>
				<div class="control__indicator"></div>
				</label>

				<label class="control control--radio column is-flex is-align-center is-flex-column-reverse">4
				<input type="radio" name="radio" checked="checked"/>
				<div class="control__indicator"></div>
				</label>	

				<label class="control control--radio column is-flex is-align-center is-flex-column-reverse" >5
				<input type="radio" name="radio" checked="checked"/>
				<div class="control__indicator"></div>
				</label>											

				</div>

				<!-- Next applicant button -->
				<a class="button is-primary is-medium" style="margin-top: 3em;">Next applicant</a>
				<div class="pad"></div>			
			</center>		
		</div>

		<!-- Information panel -->
		<div class="column has-background-light">

			<!-- Major -->
			<div class="title" style="margin: 1em;">Major</div>	
			<div class="subtitle is-4" style="margin: 1em;">{{major}}</div>
			<!-- <div class="pad-light"></div>		 -->

			<!-- Year -->
			<div class="title" style="margin: 1em;">College year</div>	
			<div class="subtitle is-4" style="margin: 1em;">{{year}}</div>	
			<!-- <div class="pad-light"></div>	 -->

			<!-- Essays -->
			<div class="title" style="margin: 1em;">Text information</div>	
			<div class="subtitle is-4" style="margin: 1em;">REPLACE ME</div>	
			<!-- <div class="pad"></div>		 -->

			<!-- Resume -->
			<div class="title" style="margin: 1em; margin-bottom: 0em;">Resume</div>															
			<iframe src="http://josharnoldjosh.github.io" width="80%" height="250em" style="overflow:auto; margin-top: 1em;"></iframe>
			<!-- <div class="pad"></div> -->

			<div class="title" style="margin: 1em;">Direct links</div>
			<!-- Resume -->
			<a class="button is-primary is-medium" style="margin-left: 1em;">Resume</a>	

			<!-- Github -->			
			<a class="button is-primary is-medium" style="margin-left: 1em;">Github</a>			

			<!-- LinkedIn -->			
			<a class="button is-primary is-medium" style="margin-left: 1em;">LinkedIn</a>							
						
			<div class="pad"></div>		
		</div>
	</div>
</div>
</template>

<script>  
export default {

}
</script>


