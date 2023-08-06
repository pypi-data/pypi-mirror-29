### Status
[![Build Status](https://travis-ci.org/imravishar/sliding_window.svg?branch=master)](https://travis-ci.org/imravishar/sliding_window)
[![PyPI](https://img.shields.io/pypi/v/window-slider.svg)](https://pypi.python.org/pypi/window-slider)
[![last commit](https://img.shields.io/github/last-commit/imravishar/sliding_window.svg?label=last%20commit)](https://github.com/imravishar/sliding_window/commits/master)
[![License](https://img.shields.io/hexpm/l/plug.svg)](https://tldrlegal.com/license/apache-license-2.0-(apache-2.0))

**Usage**
=========
    $ pip install window-slider
    
$ python

    from window_slider import Slider
    import numpy
    list = numpy.array([0, 1, 2, 3, 4, 5, 6, 7])
    bucket_size = 3
    overlap_count = 1
    slider = Slider(bucket_size,overlap_count)
    slider.fit(list)       
    while True:
        window_data = slider.slide()
        # do your stuff
        print(window_data)
        if slider.reached_end_of_list(): break

numpy 2D array
-
    from window_slider import Slider
    import numpy
    list = numpy.array([[0, 1, 2, 3],[0, 1, 2, 3]])
    bucket_size = 3
    overlap_count = 1
    slider = Slider(bucket_size,overlap_count)
    slider.fit(list)       
    while True:
        window_data = slider.slide()
        # do your stuff
        print(window_data)
        if slider.reached_end_of_list(): break

wrap window data to custom class
-
    class WindiwData(object):
        def __init__(self, data):
            self._data = data
        
        def sum(self):
            return sum(self._data)
            
    
    from window_slider import Slider
    import numpy
    list = numpy.array([0, 1, 2, 3, 4, 5, 6, 7])
    bucket_size = 3
    overlap_count = 1
    slider = Slider(bucket_size,overlap_count,WindiwData)
    slider.fit(list)       
    while True:
        window_data = slider.slide()
        # do your stuff
        print(window_data.sum())
        if slider.reached_end_of_list(): break