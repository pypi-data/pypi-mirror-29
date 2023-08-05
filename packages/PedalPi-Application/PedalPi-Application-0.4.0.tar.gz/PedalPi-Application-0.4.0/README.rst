Pedal Pi - Application
======================

.. image:: https://travis-ci.org/PedalPi/Application.svg?branch=master
    :target: https://travis-ci.org/PedalPi/Application
    :alt: Build Status

.. image:: https://readthedocs.org/projects/pedalpi-application/badge/?version=latest
    :target: http://pedalpi-application.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/PedalPi/Application/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PedalPi/Application
    :alt: Code coverage

.. image:: https://landscape.io/github/PedalPi/Application/master/landscape.svg?style=flat
    :target: https://landscape.io/github/PedalPi/Application/master
    :alt: Code Health

Pedal Pi - Application is a framework for manager the Pedal Pi.
Through it is possible loads `Pedal Pi Components`_
to provide a Human Machine Interface (HMI) or even have an opening for other software
to consume the features of the Pedal Pi.

The components developed use the API (available through `Controllers <controller.html>`__) to manage the resources of the Pedal Pi.

.. _Pedal Pi Components: https://github.com/PedalPi/Components

**Documentation:**
   http://pedalpi-application.readthedocs.io/

**Code:**
   https://github.com/PedalPi/Application

**Python Package Index:**
   https://pypi.org/project/PedalPi-Application

**License:**
   `Apache License 2.0`_

.. _Apache License 2.0: https://github.com/PedalPi/Application/blob/master/LICENSE


Running Application
-------------------

Following are the steps required to set up and run Pedal Pi - Application.

Prepare ambient
***************

Install with pip

.. code-block:: bash

    pip3 install PedalPi-Application

Create the script file that contains the code to run the application (as example ``start.py``)

.. code-block:: python

    from application.application import Application

    application = Application(path_data="data/", address='localhost')

    application.start()

    from signal import pause
    try:
        pause()
    except KeyboardInterrupt:
        application.stop()

Download, compile and install `mod-host`_. Mod-host is a *LV2 host for Jack controllable via socket or command line*.
It is developed by `Mod Devices`_, a company that also develops professional equipment for musicians.

.. _mod-host: https://github.com/moddevices/mod-host
.. _Mod Devices: https://moddevices.com/

.. code-block:: bash

    git clone https://github.com/moddevices/mod-host
    cd mod-host
    make
    make install

Run Application
***************

Start audio process. The required settings for your audio card can vary greatly.
I recommend that you try different possibilities in order to minimize the latency and number of *xruns*.

If you do not have any experience with JACK, is recommend the lecture of
`Demystifying JACK – A Beginners Guide to Getting Started with JACK`_ from **Linux Music Production**.

.. _Demystifying JACK – A Beginners Guide to Getting Started with JACK: http://libremusicproduction.com/articles/demystifying-jack-%E2%80%93-beginners-guide-getting-started-jack

.. code-block:: bash

    # In this example, is starting a Zoom g3 series audio interface
    jackd -R -P70 -t2000 -dalsa -dhw:Series -p256 -n3 -r44100 -s &
    mod-host &

Finally, start the application

.. code-block:: bash

    python3 start.py


Extending
---------

It's possible add or extends the Pedal Pi with addiction of `Component`. A component can
provides a Human Machine Interface (HMI) - like `Raspberry P0`_ - or even have an opening for other software
to consume the features of the Pedal Pi - like `WebService`_ plugin.

See the `github Components Project`_ for complete components list.

To add a component in your configuration file, download it and register it before starting the application (``application.start()``):

.. code-block:: bash

    pip3 install PedalPi-<component name>

.. code-block:: python

    from application.Application import Application
    application = Application(path_data="data/", address='localhost')

    # Loading component
    from raspberry_p0.raspberry_p0 import RaspberryP0
    application.register(RaspberryP0(application))

    # Start application
    application.start()

    # Don't stop application
    from signal import pause
    try:
        pause()
    except KeyboardInterrupt:
        # Stop components with safety
        application.stop()

Each component needs a configuration to work.
Pay attention to your documentation for details on how to set it up and use it.

.. _github Components Project: https://github.com/PedalPi/Components
.. _Raspberry P0: https://github.com/PedalPi/Raspberry-P0
.. _WebService: https://github.com/PedalPi/WebService


Delegating audio processing to other equipment
----------------------------------------------

The connection with `mod-host`_ is over `TCP`_. So it's possible to place a
machine to perform the processing and another to provide the control services.

For example, you have a **Raspberry Pi B+** and a **PC**.
 * The PC in http://10.0.0.100 will process the audio, then it will execute `jack` process,
   `mod-host` process and the audio interface will be connected to it.
 * The *RPi* will executes `Application` with `Component`, like `Raspberry P0 component`_.
   Raspberry P0 disposes a simple current pedalboard control.

.. code-block:: python

    application = Application(path_data="data/", address='10.0.0.100')

.. _Raspberry P0 component: https://github.com/PedalPi/Raspberry-P0
.. _TCP: https://en.wikipedia.org/wiki/Transmission_Control_Protocol

Creating a component
--------------------

Subsequently will be added details in the documentation on how to create a component for the Pedal Pi.
For now, you can check the blog post `Building a Pedal Pi Component - Pedalboard selector`_

.. _Building a Pedal Pi Component - Pedalboard selector: https://pedalpi.github.io/blog/building-a-pedal-pi-component-pedalboard-selector.html

Maintenance
-----------

Test
****

The purpose of the tests is:

* Check if the notifications are working, since the module plugins manager is responsible for testing the models;
* Serve as a sample basis.

.. code-block:: bash

    make test
    make test-details

Generate documentation
**********************

This project uses `Sphinx`_ + `Read the Docs`_.

You can generate the documentation in your local machine:

.. code-block:: bash

    make install-docs-requirements
    make docs

    make docs-see

.. _Sphinx: http://www.sphinx-doc.org/
.. _Read the Docs: http://readthedocs.org
