class BatchScheduler:
    _release = False
    _data = []
    _processed = []

    def _do_process(self, data):
        return data

    def _process_batch(self):
        self._processed = self._do_process(self._data)
        self._release = True

    def sumbit(self, data):
        while not self.release:
            pass