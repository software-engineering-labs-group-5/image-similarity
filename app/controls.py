from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets


class Controls:
    def __init__(self):
        self.brightness_name = "Brightness"
        self.contrast_name = "Contrast"
        self.noise_name = "Noise"

        self.brightness_init = 0
        self.contrast_init = 0
        self.noise_init = 0

        self.brightness_min = -100
        self.brightness_max = 100
        self.contrast_min = -100
        self.contrast_max = 100
        self.noise_min = 0
        self.noise_max = 100

        self.brightness_is_changing = False
        self.noise_is_changing = False
        self.contrast_is_changing = False

        self.metrics_calculation_enabled = True

        self.cur_brightness_value = self.brightness_init
        self.cur_contrast_value = self.contrast_init
        self.cur_noise_value = self.noise_init

        self.image_handler = None
        self.view = None
        self.modifications_provider = None

    def subscribe_view(self, view) -> None:
        self.view = view
        if self.image_handler is not None:
            self.view.calculate_metrics_button.clicked.connect(self.update_metrics_calculation_status)

    def subscribe_image_handler(self, image_handler) -> None:
        self.image_handler = image_handler
        if self.view is not None:
            self.view.calculate_metrics_button.clicked.connect(self.update_metrics_calculation_status)

    def subscribe_modifications_provider(self, modifications_provider) -> None:
        self.modifications_provider = modifications_provider

    def update_brightness(self, value: float) -> None:
        if value == self.cur_brightness_value:
            return
        self.view.update_brightness_label(value)
        if self.image_handler.modified_image is not None and self.brightness_is_changing is False:
            self.modifications_provider.add_change({'name': 'brightness', 'value': float(value)})
            self.modifications_provider.apply_changes()
            self.cur_brightness_value = float(value)
            self.view.display_mod_image(self.image_handler.convert_matrix_to_qimage(self.image_handler.modified_image))
            if self.metrics_calculation_enabled:
                self.image_handler.trigger_metrics_calculation()

    def update_contrast(self, value: float) -> None:
        if value == self.cur_contrast_value:
            return
        self.view.update_contrast_label(value)
        if self.image_handler.modified_image is not None and self.contrast_is_changing is False:
            self.modifications_provider.add_change({'name': 'contrast', 'value': float(value)})
            self.modifications_provider.apply_changes()
            self.cur_contrast_value = float(value)
            self.view.display_mod_image(self.image_handler.convert_matrix_to_qimage(self.image_handler.modified_image))
            if self.metrics_calculation_enabled:
                self.image_handler.trigger_metrics_calculation()

    def update_noise(self, value: float) -> None:
        if value == self.cur_noise_value:
            return
        self.view.update_noise_label(value)
        if self.image_handler.modified_image is not None and self.noise_is_changing is False:
            self.modifications_provider.add_change({'name': 'noise', 'value': float(value)})
            self.modifications_provider.apply_changes()
            self.cur_noise_value = float(value)
            self.view.display_mod_image(self.image_handler.convert_matrix_to_qimage(self.image_handler.modified_image))
            if self.metrics_calculation_enabled:
                self.image_handler.trigger_metrics_calculation()

    def load_ref_image(self) -> None:
        if self.image_handler is None:
            raise Exception("load_image", "image_handler not set")
        elif self.modifications_provider is None:
            raise Exception("load_image", "modifications_provider not set")
        path_to_image, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Choose image", "",
                                                                 "Image Files (*.png *.jpg *.bmp)")
        if path_to_image != '':
            self.view.contrast_slider.setSliderPosition(self.contrast_init)
            self.view.brightness_slider.setSliderPosition(self.brightness_init)
            self.view.noise_slider.setSliderPosition(self.noise_init)
            self.modifications_provider.reset_changes()
            self.image_handler.load_ref_image_from_file(path_to_image)
            self.image_handler.regenerate_view()
            self.view.ref_image_loaded = True
            if self.view.ref_image_loaded and self.view.mod_image_loaded:
                self.view.set_controls_enabled(True)
                self.image_handler.trigger_metrics_calculation()

    def load_mod_image(self) -> None:
        if self.image_handler is None:
            raise Exception("load_image", "image_handler not set")
        elif self.modifications_provider is None:
            raise Exception("load_image", "modifications_provider not set")
        path_to_image, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Choose image", "",
                                                                 "Image Files (*.png *.jpg *.bmp)")
        if path_to_image != '':
            self.view.contrast_slider.setSliderPosition(self.contrast_init)
            self.view.brightness_slider.setSliderPosition(self.brightness_init)
            self.view.noise_slider.setSliderPosition(self.noise_init)
            self.modifications_provider.reset_changes()
            self.image_handler.load_mod_image_from_file(path_to_image)
            self.image_handler.regenerate_view()
            self.view.mod_image_loaded = True
            if self.view.ref_image_loaded and self.view.mod_image_loaded:
                self.view.set_controls_enabled(True)
                self.image_handler.trigger_metrics_calculation()

    def update_brightness_changing_status(self):
        self.brightness_is_changing = not self.brightness_is_changing
        if not self.brightness_is_changing:
            self.update_brightness(self.view.brightness_slider.value())

    def update_noise_changing_status(self):
        self.noise_is_changing = not self.noise_is_changing
        if not self.noise_is_changing:
            self.update_noise(self.view.noise_slider.value())

    def update_contrast_changing_status(self):
        self.contrast_is_changing = not self.contrast_is_changing
        if not self.contrast_is_changing:
            self.update_contrast(self.view.contrast_slider.value())

    def update_metrics_calculation_status(self):
        self.metrics_calculation_enabled = not self.metrics_calculation_enabled
        if self.metrics_calculation_enabled:
            self.view.calculate_metrics_button.setText("Calculate metrics: On")
        else:
            self.view.calculate_metrics_button.setText("Calculate metrics: Off")

    def undo_change(self):
        change = self.modifications_provider.undo_change()
        if change['name'] == 'brightness':
            self.view.brightness_slider.setSliderPosition(change['value'])
        elif change['name'] == 'noise':
            self.view.noise_slider.setSliderPosition(change['value'])
        elif change['name'] == 'contrast':
            self.view.contrast_slider.setSliderPosition(change['value'])
        if self.view.ref_image_loaded and self.view.mod_image_loaded and self.metrics_calculation_enabled:
            self.image_handler.trigger_metrics_calculation()
