# Improving Crops Disease Classification
Our work has been accepted in Challenges & Opportunities for Computer Vision in Agriculture **CVPR Workshop, 2020.** 
<br /> Titled **"Deep Unsupervised Deblurring Approach for Improving Crops Disease Classification"** 
<br />
## Summary:
Crop diseases pose a major threat to the world food security, and their timely identification is of utmost importance. However, the prevalence of distortion and motion blur in the crop images during image acquisition make image enhancement a mandatory step. Recently, deep learning-based approaches have shown the state of the art results for image enhancement. However, one critical limitation of these deep learning-based approaches is the requirement of high-quality noiseless ground truth images
that are difficult to obtain in many agricultural applications. To solve this issue, we leverage a recently proposed deep
learning-based approach that does not require ground-truth images to remove the motion blur. We show the effectiveness of our proposed approach on wheat and rice plant disease datasets.

## Code
**How to Run**
1. Run `make_txt.ipynb`  to get paths of images in the training set and your generated blur kernels.
2. Run `train_nonblind.ipynb`  for running unsupervised deblur algorithm (proposed in paper) for your dataset.
3. Run `train_supervised.ipynb`  for running supervised deblur algorithm (proposed in paper) for your dataset.
4. Run `train_classification_model.ipynb`to train any open source deep learning model on your dataset for disease classification
5. Run `blur_deblur_and_save.ipynb` to load test images, convolve with blur kernels and deblur with your trained model and then save  both into separate directories.
6. Run `test_classifier.ipynb` to load clean, blur and deblur (by supervised & unsupervised methods) test images and test your trained classification model.

