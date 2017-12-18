Description

    file [stair_case, foot_case, final_windows] are developed at windows

    stair: it is maked for finding stair
        
        1. stair_case/source: reference code
        2. stair_case/basic: about image processing, basic edge detection, sift (not used for final code)
        3. stair_case/represent Stair: failed algorithm
        4. stair_case/using contour: automatically edge detect and draw contour box
        5. stair_case/voting: about voting algorithm, it is used to find stair(final algorithm)
        6. stair_case/voting_edge_detection.py: code for detecting stairs
        
    foot: it is maked for finding foot
    
        1. foot_case/source: about image processing
        2. foot_case/represent: failed algorithm
        3. foot_case/voting: failed algorithm
        4. foot_case/segmentation: failed algorithm
        5. foot_case/tracking: about tracking, it is provided at OpenCV
        6. foot_case/multi_trackingl.py: code for tracking foot
        
    final_windows: it is maked for finding foot and stair
    
        1. final_windows/source: about image processing
        2. final_windows/previous_version: previous version (try to combine algorithms)
        3. final_windows/final.py: code for detecting stairs and tracking foots
    
    file [final_rasp] is dveloped at raspberry pi
    
    final_rasp: it is maked for raspberry pi environment and added buzzer system
    
        1. final_rasp/basic: about controlling buzzer and camera
        2. final_rasp/finalRasp.py: code for detecting stairs and tracking foots. finally, alter warning by raspberry pi

used algorithm

    1. find stair: preprocessing, Canny Edge Detection, voting, k-means
    2. track foot: tracking
    3. alert: if shoe is over next stair, alert

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
        1. follow this URL:  https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
        
    - scipy: To use k-means algorithm, must install scipy
        1. Open terminal
        2. In terminal, "pip install scipy"
    
    - scikit-learn: To use k-means algorithm, must install scikit-learn
        1. Open terminal
        2. In terminal, "pip install -U scikit-learn"
  
---------------------------------------------------------------------------------------------------------------
Related URL abour computer vision

    - Edge detection: http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
  
    - Image filtering: http://docs.opencv.org/3.1.0/d4/d13/tutorial_py_filtering.html
    
    - Obejct tracking: https://docs.opencv.org/3.1.0/db/df8/tutorial_py_meanshift.html
                       https://www.learnopencv.com/object-tracking-using-opencv-cpp-python/
