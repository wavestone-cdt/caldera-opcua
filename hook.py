from app.utility.base_world import BaseWorld
from plugins.opc_ua.app.opc_ua_svc import opc_uaService

name = 'opc_ua'
description = 'plugin for opc_ua PLCs'
address = '/plugin/opc_ua/gui'
access = BaseWorld.Access.RED


async def enable(services):
    opc_ua_svc = opc_uaService(services, name, description)
    app = services.get('app_svc').application
    app.router.add_route('GET', '/plugin/opc_ua/gui', opc_ua_svc.splash)
    app.router.add_route('GET', '/plugin/opc_ua/data', opc_ua_svc.plugin_data)





