
class Consumer:
    def consumer_func(self, payload, *args, **kwargs):
        return self._consumer_func(payload, *args, **kwargs)

    def _consumer_func(self, payload, *args, **kwargs):
        raise NotImplementedError
