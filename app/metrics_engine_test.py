import numpy as np
import time
from metrics_engine import MetricsEngine


def test_load_metrics() -> None:
    # given
    engine = MetricsEngine()
    expected_metrics_names = sorted(['cpsnr_metric',
                                     'psnr_metric',
                                     'rmse_metric',
                                     # 'fsim_metric',
                                     'ssim_metric'])

    # when
    engine.load_metrics('../plugins')

    # then
    assert len(engine.metrics_list) == 4  # 5
    metrics_names = sorted([metric.name for metric in engine.metrics_list])
    print(metrics_names)
    assert metrics_names == expected_metrics_names
    print(f"test_load_metrics: pass")


def test_metric_compute() -> None:
    # given
    # img_1 = np.zeros((300,300,3))
    # img_2 = np.ones((300,300,3))

    # img_1 = np.random.random_sample((300,300,3))

    img_1a = np.genfromtxt('../example_array_0.csv', delimiter=',')
    img_1b = np.genfromtxt('../example_array_1.csv', delimiter=',')
    img_1c = np.genfromtxt('../example_array_2.csv', delimiter=',')
    img_1 = np.stack([img_1a, img_1b, img_1c], axis=-1)
    img_2 = img_1 * 1.05

    engine = MetricsEngine()
    engine.load_metrics('../plugins')

    expected_results = {
        'cpsnr_metric': 36.81357101978457,
        'fsim_metric': 0.9992996404431441,
        'psnr_metric': 103.0365991951924,
        'rmse_metric': 7.04969032961156e-06,
        'ssim_metric': 0.9999996107525898
    }

    # when
    start = time.time()
    results = {metric.name: metric.compute(img_1, img_2) for metric in engine.metrics_list}
    end = time.time()
    # then
    print(f"Metrics calculation took: {end - start} seconds")
    assert results == expected_results
    print(f"test_metric_compute: pass")


if __name__ == "__main__":
    test_load_metrics()
    test_metric_compute()
