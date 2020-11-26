import numpy as np

def rmse_metric(org_img: np.ndarray, pred_img: np.ndarray, max_p=4095) -> float:
    """
    Root Mean Squared Error
    Calculated individually for all bands, then averaged
    """
    #_assert_image_shapes_equal(org_img, pred_img, "RMSE")

    org_img = org_img.astype(np.float32)

    rmse_bands = []
    for i in range(org_img.shape[2]):
        dif = np.subtract(org_img, pred_img)
        m = np.mean(np.square( dif / max_p))
        s = np.sqrt(m)
        rmse_bands.append(s)

    return np.mean(rmse_bands)