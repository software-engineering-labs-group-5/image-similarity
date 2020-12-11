import numpy as np


class ModificationsProvider:
    def __init__(self):
        self.image_handler = None
        self.changes_list = []
        self.modifications = {'brightness': 0.0, 'contrast': 0.0, 'noise': 0.0}
        self.noise_matrix = None
        self.noise_level = 0.0
        self.change_to_undo = False

    def add_change(self, change: dict) -> None:
        if self.change_to_undo:
            self.change_to_undo = False
            return
        try:
            if change['name'] in self.modifications and type(change['value']) is float:
                self.modifications[change['name']] = change['value']
                self.changes_list.append(change)
            else:
                raise KeyError
        except (AttributeError, KeyError):
            raise Exception("add_change", f"invalid change passed: {change}, "
                                          f"should be e.g. {'name': 'contrast', 'value': 50.0}")

    def reset_changes(self):
        self.modifications = {'brightness': 0.0, 'contrast': 0.0, 'noise': 0.0}
        self.noise_matrix = None
        self.noise_level = 0.0
        self.changes_list.clear()

    def undo_change(self) -> dict:
        if len(self.changes_list) == 0:
            return {'name': '', 'value': 0.0}

        self.change_to_undo = True
        deleted_change = self.changes_list.pop()
        for change in reversed(self.changes_list):
            if change['name'] == deleted_change['name']:
                return change
        # The deleted change was the first one of this kind
        deleted_change['value'] = 0.0
        return deleted_change

    def apply_changes(self) -> None:
        if self.image_handler is not None:
            self.image_handler.revert_modifications()
            if self.modifications['brightness'] != 0.0:
                self.image_handler.apply_modification(self.__change_brightness__(self.modifications['brightness']))
            if self.modifications['noise'] != 0.0:
                self.image_handler.apply_modification(self.__gaussian_noise__(self.modifications['noise']))
            if self.modifications['contrast'] != 0.0:
                self.image_handler.apply_modification(self.__change_contrast__(self.modifications['contrast']))
        else:
            raise Exception("apply_changes", "image_handler is not set")

    def subscribe_image_handler(self, image_handler) -> None:
        self.image_handler = image_handler

    def __change_brightness__(self, value: float):
        return lambda image: (image + int(value * 255.0 / 100.0)).clip(min=0, max=255)

    def __change_contrast__(self, value: float):
        return lambda image: self.__change_values_scale__(-value * 1.27, 255 + value * 1.27, image).clip(min=0, max=255)

    def __change_values_scale__(self, min: float, max: float, image: np.asarray) -> np.asarray:
        return image * (max - min) / 255.0 + min

    def __gaussian_noise__(self, value: float):
        if self.noise_matrix is None or self.noise_level != value:
            mean = 0
            sigma = value / 10
            self.noise_level = value
            self.noise_matrix = np.asarray(25 * np.random.normal(mean, sigma, self.image_handler.reference_image.shape),
                                           dtype=int)
        return lambda image: (image + self.noise_matrix).clip(min=0, max=255)
