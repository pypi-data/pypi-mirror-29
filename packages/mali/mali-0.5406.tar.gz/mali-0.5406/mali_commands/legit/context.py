# -*- coding: utf8 -*-


class Expando(object):
    pass


def build_context(output_format=None, config_prefix=None, config_file=None):
    ctx = Expando()

    init_context(ctx, output_format, config_prefix, config_file)

    return ctx


def init_context(ctx, output_format=None, config_prefix=None, config_file=None):
    from .config import Config
    from .api import handle_api

    ctx.obj = Expando()

    config = Config(config_prefix, config_file)

    ctx.obj.config = config
    ctx.obj.handle_api = handle_api

    ctx.obj.api_host = config.api_host
    ctx.obj.host = config.host
    ctx.obj.client_id = config.client_id
    ctx.obj.refresh_token = config.refresh_token

    ctx.obj.auth0 = config.auth0
    ctx.obj.output_format = output_format

    ctx.obj.refresh_token = config.refresh_token
    ctx.obj.id_token = config.id_token

    ctx.obj.rm_socket_server = config.rm_socket_server
    ctx.obj.rm_config_volume = config.rm_config_volume
    ctx.obj.rm_manager_image = config.rm_manager_image
    ctx.obj.rm_container_name = config.rm_container_name
