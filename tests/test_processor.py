import pytest

from toolkit.processor import Processor, AsyncProcessor


@pytest.fixture(scope="module", params=[[183, 432, 1023], [11, 43, 59]])
def weight(request):
    return request.param


class TestProcesser(object):

    def test_split(self, weight):
        x,  y, z = Processor.split(weight, 0, 100)
        assert weight[0] // x == (weight[0] + weight[1]) // y ==\
               (weight[0] + weight[1] + weight[2])// z

    def test_processor_with_same_from_to(self, capsys):
        updated = list()

        def fun(process):
            updated.append(process)
        processor = Processor(2, fun, _from=11, to=11)
        assert processor.processes == [11, 11]
        processor.update()
        assert updated == []
        processor.update()
        assert updated == []

    def test_processor_with_weight_zero(self):
        updated = list()

        def fun(process):
            updated.append(process)
        processor = Processor(2, fun)
        assert processor.processes == [50, 100]
        processor.update()
        with processor.hand_out(0) as child:
            pass
        assert updated == [50, 100]

    @pytest.mark.asyncio
    async def test_async_processor(self):
        updated = list()
        messages = list()

        async def fun(process, message):
            updated.append(process)
            messages.append(message)

        processor = AsyncProcessor(2, fun)
        assert processor.processes == [50, 100]
        await processor.update("1")
        async with processor.hand_out(0) as child:
            pass
        assert updated == [50, 100]
        assert messages == ["1", ""]
