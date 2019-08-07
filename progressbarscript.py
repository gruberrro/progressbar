# -*- coding: utf-8 -*-

"""
Base classes used for script creation.
"""

from __future__ import print_function
from __future__ import unicode_literals

from tqdm import tqdm

import get_logger_adapter


class BaseScript(object):

    """Base class for creation of simple script."""

    log = get_logger_adapter('basescript.logger')

    def run(self, *args, **kwargs):
        """Main method run by script."""
        raise NotImplementedError


class ProgressBarScript(BaseScript):

    """Base class for creation of script with progressbar."""

    log = get_logger_adapter('progressbarscript.logger')

    def set_up(self, *args, **kwargs):
        """Method responsible for setting up context for progressbar iteration.

        :return: context for further steps
        :rtype: dict
        """
        context = {}
        return context

    def iterator(self, context=None):
        """
        Method responsible for creation object that script is iterating over.

        :param dict or None context: context passed by set_up method
        :return: context for further steps
        :rtype: dict
        """
        raise NotImplementedError

    def step(self, item, context=None):
        """
        Definition of step run for every object yielded from iterator.

        :param dict or None context: context passed by set_up method
        :return: context for further steps
        :rtype: dict
        """
        if context is None:
            context = {}
        return context

    def tear_down(self, context=None):
        """
        Method responsible for tearing down all resources used by script.

        :param dict or None context: context passed by set_up method
        """
        pass

    def run(self, *args, **kwargs):
        """Main method of script implementing iterator logic."""
        context = self.set_up(*args, **kwargs)
        for item in tqdm(self.iterator(context)):
            context = self.step(item, context)
        self.tear_down(context)
