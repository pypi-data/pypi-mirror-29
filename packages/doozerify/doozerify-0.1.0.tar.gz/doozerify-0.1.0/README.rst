#########
doozerify
#########

Are you a Henson_ user? Are you looking to take advantage of unreleased
features? Have you discovered Doozer_ and are curious to try it but are
concerned about missing extensions or the work involved in updating your
imports?

If you've answered "yes" to these questions then ``doozerify`` is for you.
``doozerify`` is a module that you can install that will make ``import`` look
for Doozer equivalents for all of your Henson imports, falling back to the
Henson version if no equivalent is found.


Installation
############

    $ pip3 install doozerify


Usage
#####

Place the following code at the beginning of the entry point to your
application::

    import doozerify
    doozerify.install()


Example
=======

.. code::

    import doozerify
    doozerify.install()

    from henson import Application


    class Consumer(object):
        async def read(self):
            return {}


    async def callback(app, message):
        return message

    app = Application('doozerified', callback=callback, consumer=consumer)
    app.run()


.. _Doozer: https://doozer.readthedocs.io
.. _Henson: https://henson.readthedocs.io
