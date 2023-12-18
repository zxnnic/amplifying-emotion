# CSC2521 Facial Animation Final Project

The project aims to develop a method for amplifying visible emotion expression in recorded videos of real humans onto animated human faces. Previous work done in animating emotions focus on distinct expressions of a single emotion over time, rarely looking at the progression of an emotion in terms of intensity. We want to explore if it is possible to identify quantifiable levels of expressed emotions on human faces and how they would map on a timeline. This project uses existing facial mapping methodologies (e.g. <a href="https://developers.google.com/mediapipe">MediaPipe1</a>, <a href="https://developer.apple.com/documentation/arkit/">Apple's ARKit</a>) for facial landmark detection and Facial Action Coding Units [1] (FACS) based action units (AU) identification. The project will explore the discrete quantizable levels of happiness, which is one of the six basic emotion.

### Code layout

All the code files are located in the `code` folder. There are several components to the code and they include

- `mean_au_analysis`: Analysis FACS curve and generation of generalized values for AU activation values 
- `maya_snippets`: Code snippets used to animate ValleyGirl and AppleFace
- `data`: CSV files extracted from ARKit for blendshape values
- `perceptual_study`: Results and analysis of our two perceptual study

### References
[1] Ekman, P., & Friesen, W. V. (1978). Facial Action Coding System (FACS) [Database record]. APA PsycTests. DOI: 10.1037/t27734-000 

