import numpy as np

def psnr_metric(org_img: np.ndarray, pred_img: np.ndarray, max_p=255) -> float:
    """
    Peek Signal to Noise Ratio, implemented as mean squared error converted to dB.
    It can be calculated as
    PSNR = 20 * log10(MAXp) - 10 * log10(MSE)
    When using 12-bit imagery MaxP is 4095, for 8-bit imagery 255. For floating point imagery using values between
    0 and 1 (e.g. unscaled reflectance) the first logarithmic term can be dropped as it becomes 0
    """
    #_assert_image_shapes_equal(org_img, pred_img, "PSNR")

    mse_bands = []
    for i in range(org_img.shape[2]):
        mse_bands.append(np.mean(np.square(org_img[:, :, i] - pred_img[:, :, i])))

    return 20 * np.log10(max_p) - 10. * np.log10(np.mean(mse_bands))