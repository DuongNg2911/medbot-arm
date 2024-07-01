MODEL_PATH="https://github.com/CVHub520/X-AnyLabeling/releases/download/v1.0.0/groundingdino_swint_ogc_quant.onnx"
DEST_DIR="models"

mkdir -p $DEST_DIR

curl -o $DEST_DIR/groundingdino_swint_ogc_quant.onnx $REPO_URL

echo "File downloaded to $DEST_DIR/groundingdino_swint_ogc_quant.onnx"