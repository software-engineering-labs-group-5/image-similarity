from skimage.metrics import structural_similarity
import numpy as np

def ssim_metric(org_img: np.ndarray, pred_img: np.ndarray, max_p=4095) -> float:
	"""
	Structural SIMularity index
	"""
	#_assert_image_shapes_equal(org_img, pred_img, "SSIM")

	if len(org_img.shape) >2:
		multichannel = True
	else:
		multichannel = False
		
	return structural_similarity(org_img, pred_img, data_range=max_p, multichannel=multichannel)