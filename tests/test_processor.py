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
