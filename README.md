# GRID Corpus Download and Preprocessing

This repository provides scripts to download, preprocess, and prepare the GRID dataset by extracting the face region in each video frame.

### Prerequisites
Before using these scripts, download the necessary face detection model:

```bash
wget -q -O detector.tflite https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite
```

### Scripts Overview
#### 1) Download GRID Dataset
Downloads the GRID dataset in HD resolution. If necessary, it also extracts the downloaded files.

```bash
python download_grid.py
```

#### 2) Divide Videos into Frames
Converts each downloaded GRID video into individual frames.

```bash
python preprocess_grid.py
```

#### 3) Prepare Dataset by Extracting Face Regions
Extracts the Region of Interest (ROI) for each frame, focusing on the face area, using detect_crop_faces.py. You can specify the desired size and position of the face region.

```bash
python prepare_grid_dataset.py
```


Note: This script can take several hours to complete, depending on your system and dataset size.
