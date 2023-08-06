from time import sleep

import schedule

from pyriver.engine.manager import EventManager
from pyriver.engine.exception import (
    NoSourceIntervalException,
    InvalidSourceIntervalException
)


class Source(EventManager):

    def schedule_processing(self, schema):
        schedules = {
            "5_second": self.second_5,
            "minutely": self.minutely,
            "hourly": self.hourly,
        }
        interval = schema.get("metadata", {}).get("interval")
        if not interval:
            raise NoSourceIntervalException("Could not create source, no scheduling interval was found in metadata.")
        schedules.get(interval, self.invalid_interval)()

    def invalid_interval(self):
        raise InvalidSourceIntervalException("Invalid source interval found in metadata.")

    def second_5(self):
        schedule.every(5).seconds.do(self.handle)

    def minutely(self):
        schedule.every(1).minutes.do(self.handle)

    def hourly(self):
        schedule.every().hour.do(self.handle)

    def run(self):
        self.schedule_processing(self.schema)
        while True:
            schedule.run_pending()
            sleep(1)
