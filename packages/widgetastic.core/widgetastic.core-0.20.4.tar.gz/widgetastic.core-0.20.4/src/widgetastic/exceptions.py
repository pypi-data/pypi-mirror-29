# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from selenium.common.exceptions import (  # NOQA
    NoSuchElementException, MoveTargetOutOfBoundsException, StaleElementReferenceException,  # NOQA
    NoAlertPresentException, UnexpectedAlertPresentException, WebDriverException)  # NOQA


class LocatorNotImplemented(NotImplementedError):
    pass


class WidgetOperationFailed(Exception):
    pass


class DoNotReadThisWidget(Exception):
    pass


class RowNotFound(IndexError):
    pass
