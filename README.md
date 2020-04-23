# Improving Crops Disease Classification
Our work has been accepted in Challenges & Opportunities for Computer Vision in Agriculture **CVPR Workshop, 2020.** 
<br /> Titled **"Deep Unsupervised Deblurring Approach for Improving Crops Disease Classification"** 
<br />
## Summary:
Crop diseases pose a major threat to the world food security, and their timely identification is of utmost importance. However, the prevalence of distortion and motion blur in the crop images during image acquisition make image enhancement a mandatory step. Recently, deep learning-based approaches have shown the state of the art results for image enhancement. However, one critical limitation of these deep learning-based approaches is the requirement of high-quality noiseless ground truth images
that are difficult to obtain in many agricultural applications. To solve this issue, we leverage a recently proposed deep
learning-based approach that does not require ground-truth images to remove the motion blur. We show the effectiveness of our proposed approach on wheat and rice plant disease datasets.


**How to Run**
1. Run `deblurring_*_algorithm_1.py`  for running algorithm 1 (proposed in paper)  for each dataset.
2. Run `deblurring_*_algorithm_2.py`  for running algorithm 2 (proposed in paper)  for each dataset.
3. Each `deblurring_*.py` file contains algorithm constants and parameters at the beginning under "constants" for experimentation purposes.
4. To produce closest range images (in paper) run `generate_range_images.py` with appropriate parameters, also included in the file.



