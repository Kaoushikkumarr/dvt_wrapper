import inspect


def test_app_module_exposes_create_app():
    """
    create_app is used by gunicorn to start the app (see: docker/files/start-service.sh)
    make sure it is exposed as expected
    """
    # can import
    from data_decoupling_automation import create_app

    # and takes zero params
    assert len(inspect.signature(create_app).parameters) == 0
