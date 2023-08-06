from flask_script import Option
from gunicorn.app.base import Application

from cloud_inquisitor.app import create_app
from cloud_inquisitor.config import dbconfig
from cloud_inquisitor.constants import NS_API
from cloud_inquisitor.plugins.commands import BaseCommand


class APIServer(BaseCommand):
    """Runs the production API server"""
    name = 'APIServer'
    ns = NS_API
    option_list = (
        Option('-H', '--host', dest='address', type=str, default=dbconfig.get('host', ns, 'localhost')),
        Option('-p', '--port', dest='port', type=int, default=dbconfig.get('port', ns, 5000)),
        Option('-w', '--workers', dest='workers', type=int, default=dbconfig.get('workers', ns, 6)),
    )

    def run(self, **kwargs):
        workers = kwargs['workers']
        address = '{0}:{1}'.format(kwargs['address'], kwargs['port'])

        class FlaskApplication(Application):
            def init(self, parser, opts, args):
                opts = {
                    'bind': address,
                    'workers': workers,
                    'worker_class': 'gthread'
                }

                return opts

            def load(self):
                app = create_app()
                app.register_plugins()
                return app

        FlaskApplication().run()
