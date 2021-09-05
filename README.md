# UnrealCV-stereo-depth-generation
Python scripts for generating synthetic stereo depth data using the UnrealCV library.

![UnrealCV stereo depth](https://github.com/ibaiGorordo/UnrealCV-stereo-depth-generation/blob/main/doc/img/unrealcvStereo.gif)

# How to use
* Download the binary scene from the model zoo: http://docs.unrealcv.org/en/master/reference/model_zoo.html
* Install pyunrealcv: `pip install unrealcv`
* Important:bangbang: Modify the **unrealcv.ini** file in the `WindowsNoEditor/RealisticRendering/Binaries/Win64` path (depending on the OS system) inside the scene folder like this:

`EnableRightEye=True`

* Run `python generate_stereo_unrealcv.py` 


# References
* **UnrealCV**: https://github.com/unrealcv/unrealcv
