import pytest
import inspect
import traceback
from trio.testing import trio_test

class _Setup:
    obj = None
    def __init__(self):
        self.cleans = []

    def addCleanup(self,p,*a,**k):
        self.cleans.append((p,a,k))

    async def __call__(self, obj):
        self.obj = obj
        obj.addCleanup = self.addCleanup
        await obj.setUp()

    async def teardown(self):
        try:
            while self.cleans:
                p,a,k = self.cleans.pop()
                await p(*a,**k)
            if self.obj is not None:
                await self.obj.tearDown()
        except Exception as exc:
            traceback.print_exc()

@pytest.fixture
async def set_me_up():
    setup = _Setup()
    try:
        yield setup
    finally:
        await setup.teardown()

# auto-trio-ize all async functions
@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if inspect.iscoroutinefunction(pyfuncitem.obj):
        pyfuncitem.obj = trio_test(pyfuncitem.obj)

