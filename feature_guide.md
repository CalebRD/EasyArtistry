## Features


### 1. txt 2 image
This is the most basic feature of the software, and by far the most common in other AI image generation software. The feature contains 3 main interfaces that all work together. 
	**a. Prompt box:**
		This is where you type what you want to see. You will likely want to use a combination of natural language and keywords. It's important to be specific, not only about subject matter but also things like composition, lighting, and style. Some models will require some kind of baseline prompt to be placed here, if you plan to use these models often, it may be worth creating a custom preset with the base prompt.
	**b. Negative-prompt box:**
		Similar to the prompt box, this is where you type what you DON'T want to see in your image. You likely won't be using natural language here. Instead, you should use lists of keywords and phrases. Most models will work best if you include things like "too many fingers", "awkward pose" and similar things. Avoid
		terms like "bad" or "weird" if possible.
	**c. Output:**
		This is where the image will be generated. It will show a preview of the image, alongside some buttons to modify the image after the fact. All images generated will be saved to the 'outputs' folder in the repo.

There are some additional features you might want to play around with.
		**a. Upscaler(HiRes-fix):**
			You will have the option to use the upscaler when generating an image. This essentially speeds up and refines the
			process by allowing the image to be generated at a lower resolution, and then scale that image up using the same
			model. This not only allows the image to be generated at usable resolutions in reasonable times, but also creates
			more refined and cohesive results.
		**b. Refiner:**
			The refiner feature is an admittedly niche feature, but still has some handy use cases. If you have multiple
			models installed, the refiner allows the generation process to switch models at some point through the generation
			process. An example use case is, let's say you have a model that creates interesting poses and compositions, but
			does not render in a style you enjoy. You could swap models to one that works in a more appropriate style halfway
			through, once its generally decided the pose and composition. 
### 2. img 2 img
This is very similar to txt 2 img in principle, however, it varies in a few key ways. Both prompt boxes work more or less as expected, and	all the presets should also work for this tab.
		**a. img2img tab:**
			This is specifically img2img under the main img2img category. This function essentially allows the user to upload an image, and then generate a new image that's influenced by both the words in the prompts boxes, as well as the uploaded image. The main use case for this would be to influence the model, either with the composition or style of a reference. 
		**b. inpaint tab:**
			This functions much more like the txt2img tab. Essentially, you fill out the prompts boxes, and you still upload a reference image. However, you also have to paint in (or mask out) an area where you want the model to generate. When you click generate the model will then fill in the area you masked out with whatever is written in the prompt boxes. Its recommended to use some blur on the mask for best results, it also might take a number of generations to get something that meshes well with the reference image, although this is pretty heavily dependent on the model being used. 
### 3. Presets
Presets are the first of Easy Artistry original features. They're purpose is a bit specific. When generating an image with stable diffusion, or pretty much any other model, to achieve best results one must typically include a number of keywords and phrases in order to ensure that the model does not fall into some of their common pitfalls. The purpose of this is to improve accessibility by not requiring artists to have to memorize all unintuitive or redundant keywords that are still necessary. 
		**a. What presets are for:**
			*General*- use this preset whenever the intended subject does not fit into any other category. This preset just signals to the model to avoid flat, boring, or incorrect generations. 
			*People*- use this when you're attempting to generate a character or person. This feature does all of the above, as well as encouraging accurate anatomy, clear faces, and sensible posing.
			*Architecture*- Use this when attempting to make inorganic environments, like buildings and cities. It's designed to facilitate inorganic shapes and clear, detailed architecture. 
			*Props*-use this when attempting to generate specific objects. This preset attempts to generate flat, "concept art" formats. If you do not want this, simply use 'general' in this place. 