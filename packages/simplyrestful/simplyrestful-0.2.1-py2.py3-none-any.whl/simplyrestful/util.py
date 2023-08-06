from importlib import import_module


def instantiate(class_string):
    module_name, class_name = class_string.rsplit('.', 1)
    try:
        module_ = import_module(module_name)
        try:
            class_ = getattr(module_, class_name)()
        except AttributeError:
            raise Exception('Class does not exist')
    except ImportError:
        raise Exception('Module does not exist')
    return class_ or None
