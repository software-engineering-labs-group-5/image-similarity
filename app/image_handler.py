from PIL import Image
import numpy as np
import copy
from PyQt5.QtGui import QImage


class ImageHandler:
    def __init__(self):
        self.reference_image = None
        self.modified_image = None
        self.view = None
        self.metrics_engine = None

    def subscribe_view(self, view) -> None:
        self.view = view

    def subscribe_metrics_engine(self, metrics_engine) -> None:
        self.metrics_engine = metrics_engine

    def load_image_from_file(self, image_path: str) -> None:
        loaded_image = Image.open(image_path)
        image_array = np.asarray(loaded_image)
        # Remove alpha channel if exists
        if image_array.shape[2] > 3:
            image_array = np.delete(image_array, 3, 2)
        self.reference_image = np.asarray(image_array, dtype=int)
        self.modified_image = copy.deepcopy(self.reference_image)

    def apply_modification(self, function) -> None:
        self.modified_image = function(self.modified_image)

    def revert_modifications(self):
        self.modified_image = copy.deepcopy(self.reference_image)

    def regenerate_view(self) -> None:
        if self.view is not None:
            self.view.display_ref_image(self.convert_matrix_to_qimage(self.reference_image))
            self.view.display_mod_image(self.convert_matrix_to_qimage(self.modified_image))
        else:
            raise Exception("regenerate_view", "view is not set")

    def trigger_metrics_calculation(self) -> None:
        if self.metrics_engine is not None:
            self.metrics_engine.calculate_metrics(self.reference_image, self.modified_image)
        else:
            raise Exception("trigger_metrics_calculation", "metrics_engine is not set")

    def convert_matrix_to_qimage(self, matrix: np.asarray):
        out = np.asarray(matrix, dtype=np.uint8)
        return QImage(out.data, out.shape[1], out.shape[0], out.strides[0], QImage.Format_RGB888)





