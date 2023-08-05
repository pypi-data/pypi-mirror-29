# -*- coding: utf8 -*-
import click
from terminaltables import PorcelainTable

from mali_commands.commons import print_as_json
from mali_commands.utilities.tables import dict_to_csv
from .commons import output_result


@click.group('auth')
def auth_commands():
    pass


@auth_commands.command('init')
@click.pass_context
@click.option('--webserver/--disable-webserver', default=True, required=False)
def init_auth(ctx, webserver):
    from .commons import pixy_flow

    ctx.obj.local_web_server = webserver

    access_token, refresh_token, id_token = pixy_flow(ctx.obj)

    ctx.obj.config.update_and_save({
        'token': {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'id_token': id_token,
        }
    })


@auth_commands.command('whoami')
@click.pass_context
def whoami(ctx):
    token_data = ctx.obj.config.token_data

    result = {
        'user_id': token_data.get('user_external_id'),
        'name': token_data.get('name'),
        'email': token_data.get('email'),
    }
    json_format = ctx.obj.output_format == 'json'
    format_tables = not json_format

    if format_tables:
        fields = ['name', 'email', 'user_id']
        table_data = list(dict_to_csv(result, fields))

        click.echo(PorcelainTable(table_data).table)
    else:
        print_as_json(result)


@auth_commands.command('resource')
@click.pass_context
@click.option('--org', required=True)
def auth_resource(ctx, org):
    import requests
    result = ctx.obj.handle_api(ctx.obj, requests.get, '{org}/resource/authorise'.format(org=org))

    output_result(ctx, result, ['token'])
