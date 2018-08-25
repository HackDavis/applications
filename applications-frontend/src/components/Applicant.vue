<template>
<div class="container">
	<div class="columns is-multiline">

		<!-- Control panel -->
		<div class="column section-column has-background-white is-4">		
			<center>
	
				<!-- Rating control -->
				<div class="subtitle is-3">Rating</div>

				<div class="columns is-mobile is-multiline has-background-light is-gapless">
					<div class="column">						
						<label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >1
						<input type="radio" name="radio" checked="checked"/>
						<div class="control__indicator"></div>
						</label>							
					</div>	

					<div class="column">
						<label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >2
						<input type="radio" name="radio" checked="checked"/>
						<div class="control__indicator"></div>
						</label>	
					</div>	

					<div class="column">
						<label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >3
						<input type="radio" name="radio" checked="checked"/>
						<div class="control__indicator"></div>
						</label>	
					</div>	

					<div class="column">
						<label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >4
						<input type="radio" name="radio" checked="checked"/>
						<div class="control__indicator"></div>
						</label>	
					</div>	

					<div class="column">
						<label class="control control--radio column  is-flex is-align-center is-flex-column-reverse" >5
						<input type="radio" name="radio" checked="checked"/>
						<div class="control__indicator"></div>
						</label>	
					</div>					
				</div>
				
				<!-- Next applicant button -->
				<a class="button is-primary is-medium" style="margin-top: 1em;">Next applicant</a>				
			</center>		
		</div>

		<!-- Information panel -->
		<div class="column has-background-light" style="border-radius: 1em;">

			<div class="columns is-centered is-multiline">
				<div class="column is-narrow">
					<div class="subtitle is-4">John Smith</div>
				</div>
				<div class="column is-narrow">
					<div class="subtitle is-4">Sophmore</div>
				</div>
				<div class="column is-narrow">
					<div class="subtitle is-4">Computer Engineering</div>
				</div>
			</div>
	
			<center>
				<div class="subtitle is-4">Direct links</div>	
			</center>
			
			<div class="columns is-mobile is-centered is-multiline">
				<div class="column is-narrow">
					<a class="button is-primary is-medium">Resume</a>		
				</div>

				<div class="column is-narrow">
					<a class="button is-primary is-medium">Github</a>		
				</div>

				<div class="column is-narrow">
					<a class="button is-primary is-medium">LinkedIn</a>		
				</div>
			</div>												
		</div>
	</div>
</div>
</template>

<script>  
export default {		
}
</script>




