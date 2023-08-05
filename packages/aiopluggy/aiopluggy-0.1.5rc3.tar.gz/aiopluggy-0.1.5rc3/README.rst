aiopluggy - A minimalist asyncio-ready plugin system
====================================================
.. image:: https://readthedocs.org/projects/aiopluggy/badge/?version=latest
    :target: http://aiopluggy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Please `read the docs`_ to learn more!


A definitive example
--------------------
.. code-block:: python

    import aiopluggy, asyncio

    hookspec = aiopluggy.HookspecMarker("myproject")
    hookimpl = aiopluggy.HookimplMarker("myproject")


    class MySpec(object):
        """A hook specification namespace.
        """
        @hookspec
        def myhook(self, arg1, arg2):
            """My special little hook that you can customize.
            """


    class Plugin_1(object):
        """A hook implementation namespace.
        """
        @hookimpl.asyncio
        async def myhook(self, arg1, arg2):
            print("inside Plugin_1.myhook()")
            return arg1 + arg2


    class Plugin_2(object):
        """A 2nd hook implementation namespace.
        """
        @hookimpl
        def myhook(self, arg1, arg2):
            print("inside Plugin_2.myhook()")
            return arg1 - arg2


    async def main():
        # create a manager and add the spec
        pm = aiopluggy.PluginManager("myproject")
        pm.register_specs(MySpec)

        # register plugins
        await pm.register(Plugin_1())
        await pm.register(Plugin_2())

        # call our `myhook` hook
        results = await pm.hook.myhook(arg1=1, arg2=2)
        print(results)


    asyncio.get_event_loop.run_until_complete(main())

.. links
.. _read the docs:
    https://aiopluggy.readthedocs.io/en/latest/
