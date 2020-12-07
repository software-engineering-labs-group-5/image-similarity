from image_handler import ImageHandler
from modifications_provider import ModificationsProvider
from controls import Controls
from metrics_engine import MetricsEngine
from main_view import *


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    controls = Controls()
    ui.subscribe_controls(controls)
    ui.setupUi(MainWindow)

    metrics_engine = MetricsEngine()
    metrics_engine.subscribe_view(ui)
    metrics_engine.load_metrics()
    controls.subscribe_view(ui)
    image_handler = ImageHandler()
    image_handler.subscribe_view(ui)
    modifications_provider = ModificationsProvider()
    modifications_provider.subscribe_image_handler(image_handler)
    controls.subscribe_image_handler(image_handler)
    controls.subscribe_modifications_provider(modifications_provider)
    image_handler.subscribe_metrics_engine(metrics_engine)

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
