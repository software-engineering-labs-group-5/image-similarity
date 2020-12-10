from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class MainView(QtWidgets.QMainWindow):
    def __init__(self, application: QtWidgets.QApplication):
        super().__init__()
        self.app = application
        self.controls = None

        self.central_widget = None
        self.input_image = None
        self.measured_image = None
        self.metrics_table = None
        self.metrics_label = None
        self.calculate_metrics_button = None
        self.menu_bar = None

        self.brightness_slider = None
        self.noise_slider = None
        self.contrast_slider = None
        self.brightness_label = None
        self.noise_label = None
        self.contrast_label = None

        self.menu_file = None
        self.action_open_image = None
        self.action_exit = None

        self.setup_ui()

    def subscribe_controls(self, controls) -> None:
        self.controls = controls
        self.setup_controls()

    def display_ref_image(self, image: QtGui.QImage) -> None:
        self.input_image.setPixmap(
            QtGui.QPixmap(image).scaled(512, 512, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def display_mod_image(self, image: QtGui.QImage) -> None:
        self.measured_image.setPixmap(
            QtGui.QPixmap(image).scaled(512, 512, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def setup_ui(self) -> None:
        # General stuff
        self.resize(1400, 820)
        self.setWindowTitle("Image Similarity")

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Images
        self.input_image = QtWidgets.QLabel(self.central_widget)
        self.input_image.setGeometry(QtCore.QRect(20, 10, 512, 512))
        self.input_image.setFrameShape(QtWidgets.QFrame.Box)

        self.measured_image = QtWidgets.QLabel(self.central_widget)
        self.measured_image.setGeometry(QtCore.QRect(868, 10, 512, 512))
        self.measured_image.setFrameShape(QtWidgets.QFrame.Box)

        # Metrics
        self.metrics_table = QtWidgets.QTableView(self.central_widget)
        self.metrics_table.setGeometry(QtCore.QRect(572, 160, 256, 211))

        self.metrics_label = QtWidgets.QLabel(self.metrics_table)
        self.metrics_label.setGeometry(QtCore.QRect(0, 0, 256, 211))
        self.metrics_label.setAlignment(QtCore.Qt.AlignCenter)
        self.metrics_label.setText("Upload image to display metrics")

        self.calculate_metrics_button = QtWidgets.QPushButton(self.central_widget)
        self.calculate_metrics_button.setGeometry(QtCore.QRect(630, 410, 140, 23))
        self.calculate_metrics_button.setEnabled(False)
        self.calculate_metrics_button.setText("Calculate metrics: On")

        # Sliders
        self.brightness_slider = QtWidgets.QSlider(self.central_widget)
        self.brightness_slider.setGeometry(QtCore.QRect(100, 580, 1200, 25))
        self.brightness_slider.setOrientation(QtCore.Qt.Horizontal)
        self.brightness_slider.setEnabled(False)

        self.noise_slider = QtWidgets.QSlider(self.central_widget)
        self.noise_slider.setGeometry(QtCore.QRect(100, 650, 1200, 25))
        self.noise_slider.setOrientation(QtCore.Qt.Horizontal)
        self.noise_slider.setEnabled(False)

        self.contrast_slider = QtWidgets.QSlider(self.central_widget)
        self.contrast_slider.setGeometry(QtCore.QRect(100, 720, 1200, 25))
        self.contrast_slider.setOrientation(QtCore.Qt.Horizontal)
        self.contrast_slider.setEnabled(False)

        font = QtGui.QFont()
        font.setPointSize(10)
        self.brightness_label = QtWidgets.QLabel(self.central_widget)
        self.brightness_label.setEnabled(True)
        self.brightness_label.setGeometry(QtCore.QRect(100, 550, 140, 21))
        self.brightness_label.setFont(font)

        self.noise_label = QtWidgets.QLabel(self.central_widget)
        self.noise_label.setEnabled(True)
        self.noise_label.setGeometry(QtCore.QRect(100, 620, 111, 21))
        self.noise_label.setFont(font)

        self.contrast_label = QtWidgets.QLabel(self.central_widget)
        self.contrast_label.setEnabled(True)
        self.contrast_label.setGeometry(QtCore.QRect(100, 690, 140, 21))
        self.contrast_label.setFont(font)

        # Menu
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1400, 21))
        self.setMenuBar(self.menu_bar)

        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setTitle("File")
        self.menu_bar.addAction(self.menu_file.menuAction())

        self.action_exit = QtWidgets.QAction(self)
        self.action_exit.triggered.connect(self.close_program)
        self.action_exit.setText("Exit")
        self.action_exit.setStatusTip("Exit from the program")
        self.action_exit.setShortcut("Ctrl+W")

        self.action_open_image = QtWidgets.QAction(self)
        self.action_open_image.setText("Open image")
        self.action_open_image.setStatusTip("Open an image from your computer")
        self.action_open_image.setShortcut("Ctrl+O")

        self.menu_file.addAction(self.action_open_image)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)

    def setup_controls(self) -> None:
        self.action_open_image.triggered.connect(self.controls.load_image)

        self.brightness_slider.setMinimum(self.controls.brightness_min)
        self.brightness_slider.setMaximum(self.controls.brightness_max)
        self.brightness_slider.valueChanged.connect(self.controls.update_brightness)
        self.brightness_slider.sliderPressed.connect(self.controls.update_brightness_changing_status)
        self.brightness_slider.sliderReleased.connect(self.controls.update_brightness_changing_status)
        self.update_brightness_label(self.brightness_slider.value())

        self.noise_slider.setMinimum(self.controls.noise_min)
        self.noise_slider.setMaximum(self.controls.noise_max)
        self.noise_slider.valueChanged.connect(self.controls.update_noise)
        self.noise_slider.sliderPressed.connect(self.controls.update_noise_changing_status)
        self.noise_slider.sliderReleased.connect(self.controls.update_noise_changing_status)
        self.update_noise_label(self.noise_slider.value())

        self.contrast_slider.setMinimum(self.controls.contrast_min)
        self.contrast_slider.setMaximum(self.controls.contrast_max)
        self.contrast_slider.valueChanged.connect(self.controls.update_contrast)
        self.contrast_slider.sliderPressed.connect(self.controls.update_contrast_changing_status)
        self.contrast_slider.sliderReleased.connect(self.controls.update_contrast_changing_status)
        self.update_contrast_label(self.contrast_slider.value())

    def display_metrics(self, metrics: dict) -> None:
        metrics_string = ""
        for metric in metrics:
            metrics_string += f"{metric['name']}: {str(round(metric['value'], 2))}\n"
        self.metrics_label.setText(metrics_string)

    def set_controls_enabled(self, status: bool) -> None:
        self.calculate_metrics_button.setEnabled(status)
        self.brightness_slider.setEnabled(status)
        self.noise_slider.setEnabled(status)
        self.contrast_slider.setEnabled(status)

    def update_brightness_label(self, value: float) -> None:
        self.brightness_label.setText(self.controls.brightness_name + ": " + str(value))

    def update_noise_label(self, value: float) -> None:
        self.noise_label.setText(self.controls.noise_name + ": " + str(value))

    def update_contrast_label(self, value: float) -> None:
        self.contrast_label.setText(self.controls.contrast_name + ": " + str(value))

    def close_program(self) -> None:
        self.app.quit()


if __name__ == "__main__":
    single_app = QtWidgets.QApplication(sys.argv)
    main_view = MainView(single_app)
    main_view.show()
    sys.exit(single_app.exec_())
