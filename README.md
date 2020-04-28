# Improving Crops Disease Classification
This repository contains the code for the workshop paper 
<br /> **"Deep Unsupervised Deblurring Approach for Improving Crops Disease Classification"** 
<br /> accepted in Computer Vision and Pattern Recognition (CVPR) 
<br /> track: Challenges & Opportunities for Computer Vision in Agriculture 2020.  
<br />  Authors **Javed Ahmad, Fahad Shamshad, Junaid Maqbool, and Ali Ahmed** 
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

## Experimental Results
**Qualitative Results on Wheat Crop**
<p align="center">
  <img src="./Images/wheat_quality.png" width="600" title="Qualitative result on wheat data">
</p>

**Qualitative Results on Rice Crop**
<p align="center">
  <img src="./Images/rice_quality.png" width="600" title="Qualitative result on wheat data">
</p>


**Quantitative Results on Rice Crop**
<table>
    <thead>
        <tr>
            <th>Crop</th>
            <th>Data</th>
            <th>PSNR</th>
            <th>SSIM</th>
            <th>GoogleNet</th>
            <th>Resnet18</th>
            <th>Alexnet</th>
            <th>VGG11</th>
            <th>Squeezenet</th>
            <th>Densenet</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=4>Wheat</td>
            <td> Clean  </td>
            <td>  -    </td>
            <td>  -    </td>
            <td>  76.66%   </td>
            <td>   84.16% </td>
            <td>  78.33% </td>
            <td>  68.33% </td>
            <td>   83.33%   </td>
            <td>  78.33%  </td>`
        </tr>
        <tr>
            <td> Blur   </td>
            <td> 16.96 </td>
            <td> 0.195 </td>
            <td>  62.50%   </td>
            <td>   71.66% </td>
            <td>  59.16% </td>
            <td>  46.66% </td>
            <td>   65.00%   </td>
            <td>  58.33%  </td>
        </tr>
        <tr>
            <td> Unsupervised </td>
            <td> 18.55 </td>
            <td> 0.483 </td>
            <td>  74.16%   </td>
            <td>   75.83% </td>
            <td>  76.66% </td>
            <td>  67.50% </td>
            <td>   77.50%   </td>
            <td>  73.33%  </td>
        </tr>
        <tr>
            <td> Supervised   </td>
            <td> 18.90 </td>
            <td> 0.494 </td>
            <td>  75.06%   </td>
            <td>   76.66% </td>
            <td>  77.50% </td>
            <td>  67.50% </td>
            <td>   78.33%   </td>
            <td>  74.16%  </td>
        </tr>
        <tr>
            <td rowspan=4> Rice  </td>
            <td> Clean  </td>
            <td>   -   </td>
            <td>  -    </td>
            <td>  78.12%   </td>
            <td>   82.50% </td>
            <td>  56.25% </td>
            <td>  83.75% </td>
            <td>   77.50%   </td>
            <td>  81.87%  </td>
        </tr>
        <tr>
            <td> Blur   </td>
            <td> 22.52 </td>
            <td> 0.73  </td>
            <td>  31.25%   </td>
            <td>   36.25% </td>
            <td>  40.62% </td>
            <td>  26.25% </td>
            <td>   25.62%   </td>
            <td>  30.00%  </td>
        </tr>
        <tr>
            <td> Unsupervised </td>
            <td> 29.63 </td>
            <td> 0.852 </td>
            <td>  53.75%   </td>
            <td>   55.00% </td>
            <td>  56.25% </td>
            <td>  52.50% </td>
            <td>   52.50%   </td>
            <td>  57.50%  </td>
        </tr>
        <tr>
            <td> Supervised   </td>
            <td> 29.77 </td>
            <td> 0.857 </td>
            <td>  54.37%   </td>
            <td>   51.25% </td>
            <td>  53.75% </td>
            <td>  56.25% </td>
            <td>   46.83%   </td>
            <td>  61.25%  </td>
        </tr>
    </tbody>
</table>
