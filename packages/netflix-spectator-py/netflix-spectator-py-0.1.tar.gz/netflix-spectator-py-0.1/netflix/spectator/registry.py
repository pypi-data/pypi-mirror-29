import logging
import math
import sys
import threading

from netflix.spectator.id import MeterId
from netflix.spectator.clock import SystemClock
from netflix.spectator.counter import Counter
from netflix.spectator.timer import Timer
from netflix.spectator.distsummary import DistributionSummary
from netflix.spectator.gauge import Gauge
from netflix.spectator.http import HttpClient

logger = logging.getLogger("spectator.Registry")


class Registry:

    def __init__(self, clock=SystemClock()):
        self._clock = clock
        self._lock = threading.RLock()
        self._meters = {}

    def clock(self):
        return self._clock

    def _new_meter(self, name, tags, meterFactory):
        with self._lock:
            if tags is None:
                tags = {}
            meterId = MeterId(name, tags)
            meter = self._meters.get(meterId, None)
            if meter is None:
                meter = meterFactory(meterId)
                self._meters[meterId] = meter
            return meter

    def counter(self, name, tags=None):
        return self._new_meter(name, tags, lambda id: Counter(id))

    def timer(self, name, tags=None):
        return self._new_meter(name, tags, lambda id: Timer(id, self._clock))

    def distribution_summary(self, name, tags=None):
        return self._new_meter(name, tags, lambda id: DistributionSummary(id))

    def gauge(self, name, tags=None):
        return self._new_meter(name, tags, lambda id: Gauge(id))

    def __iter__(self):
        with self._lock:
            return RegistryIterator(self._meters.values())

    def start(self, config=None):
        logger.info("starting registry")
        if config is None:
            logger.info("config not specified, data will not be sent")
            config = {}
        elif type(config) is not dict:
            logger.warn("invalid config specified, data will not be sent")
            config = {}
        frequency = config.get("frequency", 5.0)
        self._uri = config.get("uri", None)
        self._client = HttpClient(self, config.get("timeout", 1))
        self._timer = RegistryTimer(frequency, self._publish)
        self._timer.start()
        logger.debug("registry started with config: %s", config)
        return RegistryStopper(self)

    def stop(self):
        logger.info("stopping registry")
        self._timer.cancel()
        self._publish()

    def _publish(self):
        snapshot = {}
        for meter in self:
            snapshot.update(meter._measure())

        if logger.isEnabledFor(logging.DEBUG):
            for id, value in snapshot.items():
                logger.debug("reporting: %s => %f", id, value)

        if self._uri is not None:
            json = self._measurements_to_json(snapshot)
            self._client.post_json(self._uri, json)

    def _check_value(self, m):
        v = m['value']
        s = m['tags']['statistic']
        return not math.isnan(m['value']) and (v > 0 or s == 'gauge')

    def _measurements_to_json(self, data):
        ms = [self._measurement_to_json(id, v) for id, v in list(data.items())]
        return [m for m in ms if self._check_value(m)]

    def _measurement_to_json(self, id, value):
        tags = self._id_to_json(id)
        return {
            "op": self._operation(tags),
            "tags": tags,
            "value": value
        }

    def _operation(self, tags):
        return {
            "count": "add",
            "totalAmount": "add",
            "totalTime": "add",
            "totalOfSquares": "add",
            "percentile": "add",
            "max": "max",
            "gauge": "max",
            "activeTasks": "max",
            "duration": "max"
        }.get(tags['statistic'])

    def _id_to_json(self, meterId):
        tags = meterId.tags()
        tags['name'] = meterId.name
        return tags


class RegistryTimer:

    def __init__(self, frequency, function):
        self._frequency = frequency
        self._function = function
        self._cancelled = threading.Event()
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True

    def _run(self):
        while not self._cancelled.wait(self._frequency):
            try:
                self._function()
            except:
                e = sys.exc_info()[0]
                logger.exception("registry polling failed: %s", e)

    def start(self):
        self._thread.start()

    def cancel(self):
        self._cancelled.set()
        self._thread.join()


class RegistryStopper:

    def __init__(self, registry):
        self._registry = registry

    def __enter__(self):
        pass

    def __exit__(self, typ, value, traceback):
        self._registry.stop()


class RegistryIterator:

    def __init__(self, meters):
        self._meters = list(meters)
        self._pos = 0

    def next(self):
        # needed to work on 2.7
        return self.__next__()

    def __next__(self):
        if self._pos < len(self._meters):
            pos = self._pos
            self._pos += 1
            return self._meters[pos]
        else:
            raise StopIteration
