import asyncio
import pytest

from aiopluggy import *


hookspec = HookspecMarker("example")
hookimpl = HookimplMarker("example")


@pytest.mark.asyncio
# @pytest.mark.filterwarnings('ignore:pm.register')
async def test_async(pm: PluginManager):
    out = []

    class HookSpec(object):
        @hookspec
        def some_method(self, arg):
            pass

    class Plugin1(object):
        @hookimpl
        def some_method(self, arg):
            out.append(arg + 1)
            return arg + 1

    class Plugin2(object):
        @hookimpl
        async def some_method(self, arg):
            await asyncio.sleep(.1)
            out.append(arg + 2)
            return arg + 2

    class Plugin3(object):
        @hookimpl
        async def some_method(self, arg):
            await asyncio.sleep(.1)
            out.append(arg + 3)
            return arg + 3

    class Plugin4(object):
        @hookimpl
        async def some_method(self, arg):
            await asyncio.sleep(.1)
            out.append(arg + 4)
            return arg + 4

    class Plugin5(object):
        @hookimpl
        async def some_method(self, arg):
            await asyncio.sleep(.1)
            out.append(arg + 5)
            return arg + 5

    class Plugin6(object):
        @hookimpl
        def some_method(self, arg):
            asyncio.sleep(.1)
            out.append(arg + 6)
            return arg + 6

    pm.register_specs(HookSpec())
    pm.register(Plugin1())
    pm.register(Plugin2())
    pm.register(Plugin3())
    pm.register(Plugin4())
    pm.register(Plugin5())
    pm.register(Plugin6())
    results = await pm.hooks.some_method(arg=0)
    values = {result.value for result in results}
    assert values == {1, 2, 3, 4, 5, 6}
    assert set(out) == values


def test_sync(pm: PluginManager):
    out = []

    class HookSpec(object):
        @hookspec.sync
        def some_method(self, arg):
            pass

    class Plugin1(object):
        @hookimpl
        def some_method(self, arg):
            out.append(arg + 1)
            return arg + 1

    class Plugin2(object):
        @hookimpl.try_first
        def some_method(self, arg):
            out.append(arg + 2)
            return arg + 2

    class Plugin3(object):
        @hookimpl.try_last
        def some_method(self, arg):
            out.append(arg + 3)
            return arg + 3

    class Plugin4(object):
        @hookimpl.try_first
        def some_method(self, arg):
            out.append(arg + 4)
            return arg + 4

    class Plugin5(object):
        @hookimpl.try_last
        def some_method(self, arg):
            out.append(arg + 5)
            return arg + 5

    class Plugin6(object):
        @hookimpl
        def some_method(self, arg):
            out.append(arg + 6)
            return arg + 6

    pm.register_specs(HookSpec())
    pm.register(Plugin1())
    pm.register(Plugin2())
    pm.register(Plugin3())
    pm.register(Plugin4())
    pm.register(Plugin5())
    pm.register(Plugin6())
    results = pm.hooks.some_method(arg=0)
    values = [result.value for result in results]
    assert values == [4, 2, 6, 1, 3, 5]
    assert out == [4, 2, 6, 1, 3, 5]
