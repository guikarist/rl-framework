import inspect
from typing import Callable, List

import core


def get_config_params(init_func: Callable) -> List[str]:
    """
    Return configurable parameters in 'Agent.__init__' and 'Model.__init__' which appear after 'config'
    :param init_func: 'Agent.__init__' or 'Model.__init__'
    :return: A list of configurable parameters
    """

    if init_func is not core.Agent.__init__ and init_func is not core.Model.__init__:
        raise ValueError("Only accepts 'Agent.__init__' or 'Model.__init__'")

    sig = list(inspect.signature(init_func).parameters.keys())

    config_params = []
    config_part = False
    for param in sig:
        if param == 'config':
            # Following parameters should be what we want
            config_part = True
        elif config_part:
            config_params.append(param)

    return config_params
