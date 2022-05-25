# SpeedTCC

## How it works

## Image Pre-processing

<img src="docs/imgs/pre-processing.gif" width="58%" />

## Image processing

The next steps can be performed independently. From now on, we work with three images, one for each track/lane.

### Apply new Perspective

Applying a new perspective to linearize object detection. It makes tracking and speed calculation easier and more reliable.

<p float="middle">
  <img src="docs/imgs/5-lane1-histogram_equalization.png" width="18%" /> 
  <img src="docs/imgs/5-lane2-histogram_equalization.png" width="18%" /> 
  <img src="docs/imgs/5-lane3-histogram_equalization.png" width="18%" />
</p>

### Apply Foreground Mask

Apply Foreground Mask to highlight pixels that have changed from previous frames.

<p>
  <img src="docs/imgs/6-lane1-fgmask.png" width="18%" />
  <img src="docs/imgs/6-lane2-fgmask.png" width="18%" /> 
  <img src="docs/imgs/6-lane3-fgmask.png" width="18%" />
</p>

### Apply Eroded Mask

Apply Eroded Mask to remove noise.

<p>
  <img src="docs/imgs/7-lane1-erodedmask.png" width="18%" />
  <img src="docs/imgs/7-lane2-erodedmask.png" width="18%" /> 
  <img src="docs/imgs/7-lane3-erodedmask.png" width="18%" />
</p>

### Apply Dilated Mask

Apply Dilated Mask to highlight the vehicle/object

<p>
  <img src="docs/imgs/8-lane1-dilatedmask.png" width="18%" />
  <img src="docs/imgs/8-lane2-dilatedmask.png" width="18%" /> 
  <img src="docs/imgs/8-lane3-dilatedmask.png" width="18%" />
</p>

### Apply Convex Hull

Apply convex hull to smooth edges.

<p>
  <img src="docs/imgs/9-lane1-convexhull.png" width="18%" />
  <img src="docs/imgs/9-lane2-convexhull.png" width="18%" /> 
  <img src="docs/imgs/9-lane3-convexhull.png" width="18%" />
</p>

### GIF to ilustrate

<img src="docs/imgs/tracking/tracking.gif" width="28%" />

### Calculate the speed

In order to calculate the vehicle speed we use the center points and frame quantity.

---

## Installing

```sh
git clone https://github.com/brochj/SpeedTCC.git
cd SpeedTCC
```

#### 1. Create a virtual environment

```sh
python -m venv .venv
```

#### 2. Activate the virtual environment

##### On Linux or MacOs, using bash

```sh
source .venv/bin/activate
```

##### On Windows using the Command Prompt:

```sh
.venv\Scripts\activate.bat
```

##### On Windows using PowerShell:

```sh
.venv\Scripts\Activate.ps1
```

#### 3. Installing the dependencies

```sh
pip install -r requirements.txt
```

#### 4. Download the Videos
