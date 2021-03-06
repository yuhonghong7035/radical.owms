
.. _chapter_plugin_writing

********************
Writing Troy Plugins
********************

.. note::

   This part of the Troy documentation is not for *users* of Troy, but rather
   for implementors of Troy plugins.



.. _plugin_structure:

Plugin Structure
----------------

A Troy plugin is a Python module with well defined structure.  The
module must expose a class ``PLUGIN_CLASS``, and a dictionary ``PLUGIN_DESCRIPTION``, similar to this::

    import troy

    PLUGIN_DESCRIPTION = {
        'type'        : 'overlay_provisioner',
        'name'        : 'azure',
        'version'     : '0.1',
        'description' : 'This is the Azure VM provisioner.'
      }

    class PLUGIN_CLASS (troy.PluginBase) :

        def __init__ (self) :
            troy.PluginBase.__init__ (self, PLUGIN_DESCRIPTION)

        def init (self) :
            # this method is optional, do some env checking here if needed
            pass

        def provision (self, overlay) :
            # this is a method specfic to the overlay_provisioner plugin type
            raise RuntimeError ("not implemented")
        

What specific methods a plugin has to implement depends on the respective plugin
type -- simplest approach is to copy the respective default plugin and customize
the existing methods.



.. _plugin_registration:

Plugin Registration
-------------------

Troy plugins are automatically loaded once they ar installed in the correct
location -- i.e. once they are placed next to the existing plugins, with the
same naming scheme.



.. _plugin_exceptions:

Exception Handling
------------------

Plugins should never to terminate an application, e.g. via `sys.exit()`.
Instead, plugins should raise exceptions, preferably native python exceptions
such as `RunttimError` or `TypeError` etc.  Troy may convert any plugin
exceptions into warnings, and attempt may attempt to continue operation.  Troy
may also try to call the plugin again.



.. _plugin_logging:

Plugin Logging
--------------

Plugins have access to the Troy logging system::

    troy.logger.info ("loading plugin my_plugin")


