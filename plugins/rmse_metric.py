import numpy as np

def rmse_metric(org_img: np.ndarray, pred_img: np.ndarray, max_p=255) -> float:
	"""
	Root Mean Squared Error
	Calculated individually for all bands, then averaged
	"""
	#_assert_image_shapes_equal(org_img, pred_img, "RMSE")

	rmse_bands = []
	for i in range(org_img.shape[2]):
		dif = np.subtract(org_img, pred_img)
		m = np.mean(np.square(dif))
		s = np.sqrt(m)
		rmse_bands.append(s)

	return np.mean(rmse_bands)