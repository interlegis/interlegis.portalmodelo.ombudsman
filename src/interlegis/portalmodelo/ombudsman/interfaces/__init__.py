# -*- coding: utf-8 -*-
from .claim import IClaim  # noqa
from .ombudsoffice import IOmbudsOffice  # noqa
from zope.interface import Interface


class IBrowserLayer(Interface):
    """Layer especifico para este add-on.
    """
