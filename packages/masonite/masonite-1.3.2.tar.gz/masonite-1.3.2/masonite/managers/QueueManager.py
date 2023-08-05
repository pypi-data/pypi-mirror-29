from masonite.managers.Manager import Manager
from masonite.exceptions import DriverNotFound

class QueueManager(Manager):
    
    def create_driver(self, driver=None):
        if not driver:
            driver = self.container.make('QueueConfig').DRIVER.capitalize()
        else:
            driver = driver.capitalize()

        try:
            self.manage_driver = self.container.make('Queue{0}Driver'.format(driver))
        except KeyError:
            raise DriverNotFound(
                'Could not find the Queue{0}Driver from the service container. Are you missing a service provider?'.format(driver))
