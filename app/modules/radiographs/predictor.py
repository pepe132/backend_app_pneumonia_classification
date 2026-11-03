from functools import lru_cache
from io import BytesIO
from pathlib import Path
from threading import Lock

from app.core.config import CNN_MODEL_PATH


CLASS_NAMES = {
    0: "covid_19",
    1: "normal",
    2: "pneumonia_bacterial",
    3: "pneumonia_viral",
}
PREDICTION_LOCK = Lock()


class ImageModelUnavailableError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _load_model():
    model_path = Path(CNN_MODEL_PATH)
    if not model_path.is_file():
        raise ImageModelUnavailableError(
            f"No se encontró el modelo CNN en: {model_path}"
        )

    try:
        import tensorflow as tf
    except ImportError as exc:
        raise ImageModelUnavailableError(
            "TensorFlow no está instalado en el entorno del backend."
        ) from exc

    return tf.keras.models.load_model(model_path, compile=False)


def _prepare_image(image_bytes: bytes):
    try:
        import cv2
        import numpy as np
        from PIL import Image, UnidentifiedImageError
        from tensorflow.keras.applications.densenet import preprocess_input
    except ImportError as exc:
        raise ImageModelUnavailableError(
            "Faltan dependencias para procesar radiografías."
        ) from exc

    try:
        with Image.open(BytesIO(image_bytes)) as image:
            image = image.convert("RGB").resize((224, 224))
            image_array = np.asarray(image, dtype="uint8")
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("El archivo no contiene una imagen válida.") from exc

    gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    rgb_image = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB).astype("float32")

    processed = preprocess_input(rgb_image)
    return np.expand_dims(processed, axis=0)


def predict_radiograph(image_bytes: bytes) -> dict:
    try:
        import numpy as np
    except ImportError as exc:
        raise ImageModelUnavailableError(
            "NumPy no está instalado en el entorno del backend."
        ) from exc

    model_input = _prepare_image(image_bytes)
    model = _load_model()
    with PREDICTION_LOCK:
        probabilities = model.predict(model_input, verbose=0)[0]

    if len(probabilities) != len(CLASS_NAMES):
        raise ImageModelUnavailableError(
            "La salida del modelo CNN no contiene las cuatro clases esperadas."
        )

    class_index = int(np.argmax(probabilities))
    probability_values = [float(value) for value in probabilities]

    return {
        "image_class": CLASS_NAMES[class_index],
        "confidence": round(probability_values[class_index], 6),
        "prob_covid": round(probability_values[0], 6),
        "prob_normal": round(probability_values[1], 6),
        "prob_bacterial": round(probability_values[2], 6),
        "prob_viral": round(probability_values[3], 6),
        "pneumonia_probability": round(
            probability_values[2] + probability_values[3],
            6,
        ),
        "model_version": Path(CNN_MODEL_PATH).name,
    }
