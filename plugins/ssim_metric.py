from skimage.metrics import structural_similarity
import numpy as np

def ssim_metric(org_img: np.ndarray, pred_img: np.ndarray) -> float:
	"""
	Structural SIMularity index
	"""
	#_assert_image_shapes_equal(org_img, pred_img, "SSIM")

	if len(org_img.shape) >2:
		multichannel = True
	else:
		multichannel = False
	org_img = org_img.astype(np.uint8)
	pred_img = pred_img.astype(np.uint8)
	return structural_similarity(org_img, pred_img, multichannel=multichannel)