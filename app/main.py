from image_handler import ImageHandler
from modifications_provider import ModificationsProvider
from controls import Controls
from metrics_engine import MetricsEngine
from main_view import *


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_view = MainView(app)
    controls = Controls()
    main_view.subscribe_controls(controls)

    metrics_engine = MetricsEngine()
    metrics_engine.subscribe_view(main_view)
    metrics_engine.load_metrics()
    controls.subscribe_view(main_view)
    image_handler = ImageHandler()
    image_handler.subscribe_view(main_view)
    modifications_provider = ModificationsProvider()
    modifications_provider.subscribe_image_handler(image_handler)
    controls.subscribe_image_handler(image_handler)
    controls.subscribe_modifications_provider(modifications_provider)
    image_handler.subscribe_metrics_engine(metrics_engine)

    main_view.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
