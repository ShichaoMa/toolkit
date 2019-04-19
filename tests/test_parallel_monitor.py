from toolkit.monitors import ParallelMonitor


class TestParallelMonitor:

    def test_logger(self):
        assert ParallelMonitor().logger is not None
