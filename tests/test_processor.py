import pytest

from toolkit.processor import Processor


@pytest.fixture(scope="module", params=[[183, 432, 1023], [11, 43, 59]])
def weight(request):
    return request.param


class TestProcesser(object):

    def test_split(self, weight):
        x,  y, z = Processor.split(weight, 0, 100)
        assert weight[0] // x == (weight[0] + weight[1]) // y ==\
               (weight[0] + weight[1] + weight[2])// z

    def test_processor_with_same_from_to(self, capsys):
        processor = Processor(2, print, _from=11, to=11)
        assert processor.processes == [11, 11]
        processor.update()
        captured = capsys.readouterr()
        assert captured.out == ""
        processor.update()
        assert captured.out == ""
