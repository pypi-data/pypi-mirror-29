''' A AppProvider Service Provider '''
from masonite.provider import ServiceProvider
from masonite.request import Request
from masonite.routes import Route
from config import storage
from routes import web, api

class AppProvider(ServiceProvider):

    def register(self):
        self.app.bind('WebRoutes', web.ROUTES)
        self.app.bind('ApiRoutes', api.ROUTES)
        self.app.bind('Response', None)
        self.app.bind('Storage', storage)
        self.app.bind('Route', Route())
        self.app.bind('Request', Request())

    def boot(self, Environ, Request, Route):
        Route.load_environ(Environ)
        Request.load_environ(Environ).load_app(self.app)
