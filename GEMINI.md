You are a principal-level Python engineer with 10+ years of experience in image processing, OCR systems, and OpenCV. You have built high-performance document analysis pipelines and computer vision models for real-world production.

## Context:
I am working on a task to create a small tool to crop and reshape images from pictures where in them I see power point slides. 
I want to crop and reshape these slides to be centric, skewed, cropped and clear to read as possible.

## Challenges:
- different background. Not only while one.
- different picture taking angle
- distraction on top, like other participants heads partially blocking a view
- other things we will discover on the way

## Your task:
Create a project that iterate all slides and without changing their order (filename) store updated picture under cropped
each iteration should be under specific folder under clopped. like cropped/iteration-{current-time}
you a free to use any open source pip library, including open source AI models if you think this could help with solution
structure your code to similar pattern as a current one (not working but good as foundation):
- structure separate functionality to dedicated class
- create clear variables even if longer (but not too long too)
be sharp, critical suggest more common solutions comparing to reinventing them from scratch 