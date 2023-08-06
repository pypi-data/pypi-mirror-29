
from .run import flask_app
from .wrapper_api import *
import gunicorn.app.base
from gunicorn.six import iteritems
import multiprocessing


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class RunBotApplication(gunicorn.app.base.BaseApplication):

    """ Custom gunicorn application to serve the bot

        see http://docs.gunicorn.org/en/stable/custom.html
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(RunBotApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class Application():
    """ Interface to run the bot 
    """

    def run(self,host,port,set_menu=None,enable_text=True):
        # send 'get_started' button request and run the bot
        # since everything will be loaded, no exception will be raised
        from .api import get_started_btn,send_menu
        from .helpers import simple_menu
        simple_menu["persistent_menu"][0]["composer_input_disabled"] = enable_text
        get_started_btn()
        if set_menu is None:
            # use the in-built menu
            # only triggers the @get_started()
            send_menu(simple_menu)
        else:
            send_menu(set_menu)

        options = {
        'bind': '{}:{}'.format('{}'.format(host), '{}'.format(port)),
        'workers': number_of_workers(),
        }

        print("Running bot at http://{}:{}".format(host,port))
        RunBotApplication(flask_app,options).run()
