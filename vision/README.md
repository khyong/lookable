    file [stair_case, foot_case, final_windows] are developed at windows
    file [final_rasp] is dveloped at raspberry pi

detail Environment
    - Windows 10 x64 bit
    - Raspberry pi 3 b+

---------------------------------------------------------------------------------------------------------------
Download (windows)

Utility

    - python 3.6.x: https://www.python.org/downloads/release/python-362/
  
required library

    - numpy: 
        1. Open CMD
        2. In CMD window, "pip install numpy"
    
    - matplotlib: 
        1. Open CMD
        2. In CMD window, "python -mpip install -U pip"
        3. In CMD window, "python -mpip install -U matplotlib"
    
    - opencv 3.x: It is used for computer vision
        1. Download "opencv_python‑3.3.x‑cp36‑cp36m‑win_amd64.whl" file at http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
        2. Put This file in CMD path
        3. In CMD window, "pip install opencv_python-3*win_amd64.whl"
    
    - opencv_contrib 3.x: It is used for some extra algorithm such as tracking
        1. Download "opencv_python‑3.3.x+contrib‑cp36‑cp36m‑win_amd64.whl" file at http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
            => you should download the same version of opencv 3.x
        2. Put This file in CMD path
        3. In CMD window, "opencv_python‑3.3.*+contrib‑cp36‑cp36m‑win_amd64.whl"
  
    - scipy: To use k-means algorithm, must install scipy
        1. Open CMD
        2. In CMD window, "pip install scipy"
    
    - scikit-learn: To use k-means algorithm, must install scikit-learn
        1. Open CMD
        2. In CMD window, "pip install -U scikit-learn"
  
---------------------------------------------------------------------------------------------------------------
Download (raspberry pi)

required library

    - opencv 3.x and opencv_contrib 3.x: It is used for computer vision
        1. follow this URL: https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
        
    - scipy: To use k-means algorithm, must install scipy
        1. Open terminal
        2. In terminal, "pip install scipy"
    
    - scikit-learn: To use k-means algorithm, must install scikit-learn
        1. Open terminal
        2. In terminal, "pip install -U scikit-learn"
  
---------------------------------------------------------------------------------------------------------------
Description

    - SIFT: to detect user's foot, find keypoint of foot by using SIFT algorithm
    - https://docs.opencv.org/3.3.0/da/df5/tutorial_py_sift_intro.html
    - for using SIFT in opencv, download library: https://github.com/opencv/opencv_contrib/tree/master/modules/xfeatures2d

algorithm

    1. find descriptors of image and template using SIFT
    2. match those descriptors using brute force
    
    url = https://docs.opencv.org/trunk/dc/dc3/tutorial_py_matcher.html


additional url = https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/

install opencv in raspberry pi 3 = http://webnautes.tistory.com/916

---------------------------------------------------------------------------------------------------------------
Related URL abour computer vision

    - Edge detection: http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
  
    - Image filtering: http://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
    
    - Obejct tracking: https://docs.opencv.org/3.1.0/db/df8/tutorial_py_meanshift.html
                       https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
