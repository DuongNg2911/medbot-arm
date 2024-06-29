# medbot-arm
A robotic arm that can bring medical supplies to humans using speech-to-text and object detection.

## Installing dependencies
### 1. Create conda environment 
```
conda create -n yourenv python=3.10
conda activate yourenv
```
### 2. Installing required package
```
pip install -r requirements.txt
```
### 3. Download model
```
bash scripts/download_models.sh
```
### 4. Run program locally
```
cd controllers
fastapi dev
```
