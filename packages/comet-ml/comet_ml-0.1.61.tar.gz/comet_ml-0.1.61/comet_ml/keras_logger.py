import sys

from comet_ml import config


def fit_logger(real_fit):
    def wrapper(*args, **kwargs):
        if (config.experiment):
            callback = config.experiment.keras_callback()
            if 'callbacks' in kwargs and kwargs['callbacks'] is not None:
                kwargs['callbacks'].append(callback)
            else:
                kwargs['callbacks'] = [callback]

        return real_fit(*args, **kwargs)

    return wrapper


def patch(module_finder):
    module_finder.register('keras.models', 'Model.fit', fit_logger)


if "keras" in sys.modules:
    raise SyntaxError("Please import Comet before importing any keras modules")
