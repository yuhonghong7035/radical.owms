

import radical.utils as ru

from   troy.constants import *
import troy


# ------------------------------------------------------------------------------
#
PLUGIN_DESCRIPTION = {
    'type'        : 'workload_scheduler', 
    'name'        : 'first', 
    'version'     : '0.1',
    'description' : 'this is an empty scheduler which basically does nothing.'
  }


# ------------------------------------------------------------------------------
#
class PLUGIN_CLASS (troy.PluginBase):

    __metaclass__ = ru.Singleton


    # --------------------------------------------------------------------------
    #
    def __init__ (self) :

        troy.PluginBase.__init__ (self, PLUGIN_DESCRIPTION)


    # --------------------------------------------------------------------------
    #
    def schedule (self, workload, overlay) :

        # schedule to first available pilot

        if  not overlay.pilots.keys() :
            troy._logger.warn ("no pilots in overlay")
            return

        # schedule to first pilot
        pilot_id = overlay.pilots.keys()[0]

        for tid in workload.tasks.keys () :

            task = workload.tasks[tid]

            for unit_id in task.units :

                troy._logger.info ("workload schedule : assign unit %-18s to %s" % (unit_id, pilot_id))
                unit = task.units[unit_id]
                unit._bind (pilot_id)


# ------------------------------------------------------------------------------

