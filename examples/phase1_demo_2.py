
__author__    = "RADICAL Development Team"
__copyright__ = "Copyright 2013, RADICAL"
__license__   = "MIT"


"""
Demo application for 1 feb 2014 - Bag of Task (BoT)
"""

import sys
import time
import radical.owms
import getpass


PLUGIN_OVERLAY_DERIVE       = 'concurrent'
PLUGIN_OVERLAY_SCHEDULER    = 'round_robin'
PLUGIN_OVERLAY_TRANSLATOR   = radical.owms.AUTOMATIC
PLUGIN_OVERLAY_PROVISIONER  = 'sagapilot'
PLUGIN_WORKLOAD_SCHEDULER   = radical.owms.AUTOMATIC
PLUGIN_WORKLOAD_DISPATCHER  = 'sagapilot'


# ------------------------------------------------------------------------------
def create_task_description (r, msg) :
    """
    litte helper which creates a task description for a radical member greeting
    """

    task_descr                   = radical.owms.TaskDescription ()
    task_descr.tag               = "%s" % r
    task_descr.executable        = '/bin/echo'
    task_descr.arguments         = ['Hello', msg, r, '!']
    task_descr.working_directory = "%(home)s/radical_owms_demo"

    return task_descr


# ------------------------------------------------------------------------------
#
#
#
if __name__ == '__main__' :

    radical_students = ['Melissa Romanus',  'Ashley Zebrowski',   'Dinesh Ganapathi',   
                        'Mark Santcroos',   'Antons Treikalis',   'Jeffery Rabinowitz', 
                        'Patrick Gray',     'Vishal Shah',        'Radicalobot']

    radical_oldfarts = ['Shantenu Jha',     'Andre Merzky',       'Ole Weidner',
                        'Andre Luckow',     'Matteo Turilli']

    radical_students = ['Melissa Romanus',  'Ashley Zebrowski',   'Dinesh Ganapathi']
    radical_oldfarts = ['Shantenu Jha',     'Andre Merzky',       'Ole Weidner']

    # create a session with custom config options
    session = radical.owms.Session ({
        'planner' : {
            'derive' : { 
                'concurrent' : {
                    'concurrency' : '100'
                    }
                }
            }, 
        'overlay_manager' : {
            'overlay_scheduler' : {
                'round_robin' : {
                  # 'resources' : "pbs+ssh://sierra.futuregrid.org"
                    'resources' : "fork://localhost"
                    }
                }
            }
        })

    # create planner, overlay and workload manager, with plugins as configured
    planner      = radical.owms.Planner         (session)
    workload_mgr = radical.owms.WorkloadManager (session)
    overlay_mgr  = radical.owms.OverlayManager  (session)


    # --------------------------------------------------------------------------
    # Create the student workload first.  Makes sense, amiright?
    # Create two task for every radical student.  They love getting more tasks!
    workload_1 = radical.owms.Workload (session=session)

    for r in radical_students :
        workload_1.add_task (create_task_description (r+'_1', 'student       '))
        workload_1.add_task (create_task_description (r+'_2', 'future oldfart'))


    # Initial description of the overlay based on the workload, and translate the
    # overlay into N pilot descriptions.
    overlay_descr = planner.derive_overlay (workload_1.id)
    overlay       = radical.owms.Overlay           (session, overlay_descr)

    # make sure the overlay is properly represented by pilots
    overlay_mgr.translate_overlay   (overlay.id)


    # Translate 1 workload into N tasks and then M ComputeUnits, and bind them 
    # to specific pilots (which are not yet running, thus early binding)
    workload_mgr.expand_workload    (workload_1.id)
    workload_mgr.translate_workload (workload_1.id, overlay.id)
    workload_mgr.bind_workload      (workload_1.id, overlay.id,
            bind_mode=radical.owms.EARLY)

    # Schedule pilots on the set of target resources, then instantiate Pilots as
    # scheduled
    overlay_mgr.schedule_overlay   (overlay.id)
    overlay_mgr.provision_overlay  (overlay.id)

    # ready to dispatch first workload on the overlay
    workload_mgr.dispatch_workload (workload_1.id, overlay.id)


    # --------------------------------------------------------------------------
    # Now take care of the oldfart workload -- not so many tasks for the old
    # people, and we lazily reuse the same overlay -- which is running, so,
    # late binding in this case.
    workload_2 = radical.owms.Workload (session)

    for r in radical_oldfarts :
        workload_2.add_task (create_task_description (r, 'oldfart'))


    # Translate expand, translate and bind workload again, and immediately
    # dispatch it, too.  We could have used
    # different plugins here...
    workload_mgr.expand_workload    (workload_2.id)
    workload_mgr.translate_workload (workload_2.id, overlay.id)
    workload_mgr.bind_workload      (workload_2.id, overlay.id,
            bind_mode=radical.owms.LATE)
    workload_mgr.dispatch_workload  (workload_2.id, overlay.id)


    # --------------------------------------------------------------------------
    # Of course nothing will fail due to radical.owms's magic robustness and
    # and we therefore just wait until its done!
    state_1 = workload_1.state
    state_2 = workload_2.state

    while state_1 not in [radical.owms.DONE, radical.owms.FAILED] or \
          state_2 not in [radical.owms.DONE, radical.owms.FAILED] :

        radical.owms._logger.info  ("workload_1 state: %s)" % state_1)
        radical.owms._logger.info  ("workload_2 state: %s)" % state_2)

        state_1 = workload_1.state
        state_2 = workload_2.state

        time.sleep (1)


    # 'analyse' the results
    if workload_1.state == radical.owms.DONE and \
       workload_2.state == radical.owms.DONE : 
        radical.owms._logger.info  ("workload_1 done")
        radical.owms._logger.info  ("workload_2 done")

    else :
        radical.owms._logger.error ("workload(s) failed!")
        radical.owms._logger.info  ("workload_1 state: %s)" % workload_1.state)
        radical.owms._logger.info  ("workload_2 state: %s)" % workload_2.state)

    # --------------------------------------------------------------------------
    # We are done -- clean up
    workload_mgr.cancel_workload (workload_1.id)
    workload_mgr.cancel_workload (workload_2.id)
    overlay_mgr .cancel_overlay  (overlay.id)


    # --------------------------------------------------------------------------
    # We are done -- save traces
    session.timed_dump ()
    session.timed_store ('mongodb://ec2-184-72-89-141.compute-1.amazonaws.com:27017/timing/')


    # --------------------------------------------------------------------------

