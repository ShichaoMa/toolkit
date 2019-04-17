import unittest

from toolkit.service.monitors import ParallelMonitor


class ParallelMonitorTest(unittest.TestCase):

    def setUp(self):
        self.pl = ParallelMonitor()

    def test_logger(self):
        self.assertIsNotNone(self.pl.logger)
        self.pl.logger.info("成功生成logger实例！")