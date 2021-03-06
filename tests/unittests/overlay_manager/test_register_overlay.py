

__author__    = "Andre Merzky"
__copyright__ = "Copyright 2013, The SAGA Project"
__license__   = "MIT"


import radical.utils.testing as rut

import troy

# ------------------------------------------------------------------------------
#
def test_overlay_create () :
    """ 
    test overlay creation
    """
    ol1  = troy.Overlay ()
    olid = ol1.id

    troy.OverlayManager.register_overlay  (ol1)
    ol2 = troy.OverlayManager.get_overlay (olid)

    assert ol1 == ol2, "%s == %s" % (ol1, ol2)

    troy.OverlayManager.unregister_overlay (olid)

    try :
        ol2 = troy.OverlayManager.get_overlay (olid)
        assert False, "Expected LookupError, got nothing"

    except LookupError :
        pass

    except Exception as e :
        assert False, "Expected LookupError, got %s" % e

