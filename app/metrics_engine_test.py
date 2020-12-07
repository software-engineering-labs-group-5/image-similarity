import numpy as np

from metrics_engine import MetricsEngine

def test_load_metrics():
	# given
	engine = MetricsEngine()
	expected_metrics_names = sorted(['psnr_metric', 'rmse_metric', 'fsim_metric'])

	# when
	engine.load_metrics('../plugins')

	# then
	assert len(engine.metrics_list) == 3
	metrics_names = sorted([metric.name for metric in engine.metrics_list])
	print(metrics_names)
	assert metrics_names == expected_metrics_names
	print(f"test_load_metrics: pass")


def test_metric_compute():
	# given
	img_1 = np.zeros((3,3,3))
	img_2 = np.ones((3,3,3))
	
	engine = MetricsEngine()
	engine.load_metrics('../plugins')

	expected_results = {
		'fsim_metric': np.float64('nan'),
		'psnr_metric': 72.24507812192874,
		'rmse_metric': 0.0002442002442002442
	}

	# when
	results = {metric.name: metric.compute(img_1, img_2) for metric in engine.metrics_list}
	print(results)
	print(expected_results)
	print(type(results['fsim_metric']))
	print(type(expected_results['fsim_metric']))
	# then
	if results['fsim_metric'] == expected_results['fsim_metric']:
		print("dasfdagfsfdasdasdawf")
	assert results == expected_results
	print(f"test_metric_compute: pass")

if __name__ == "__main__":
	test_load_metrics()
	test_metric_compute()