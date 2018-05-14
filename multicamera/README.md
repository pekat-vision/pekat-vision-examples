# Multi camera
There is no direct support for multiple cameras in PEKAT VISION but you can use a simple workaround.

1. You simply merge images from multiple cameras to one big image (in run.sh).
2. Send the big image to PEKAT VISION by the HTTP interface (in run.sh).
3. In PEKAT VISION Flow you add a code block. In the code you split the big image back to original images (in project).


### Note:
As soon as you performed the step 3. remember the input of your project is image merged from multiple images.
That means unless you do not change project flow you need to pass always merged image to the input of the program - even for training of models.  
