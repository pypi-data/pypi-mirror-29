settings = dict(
    DATABASE='postgresql://postgres:postgres@localhost/simply_restful',
    HOST='0.0.0.0',
    PORT=5000,
    DATE_FORMAT='%Y-%m-%dT%H:%M:%S.%fZ',
    DEFAULT_AUTHENTICATION=['simplyrestful.authenticators.NullAuthenticator'],
    DEFAULT_AUTHORIZATION=[],
    DEFAULT_PAGE_SIZE=10,
    MAX_PAGE_SIZE=100
)


def configure_from_module(user_settings_module_name):
    import importlib

    mod = importlib.import_module(user_settings_module_name)

    user_defined_settings = dict(
        [
            (name, cls)
            for name, cls
            in mod.__dict__.items()
            if not name.startswith('_')
        ]
    )

    settings.update(user_defined_settings)
