#!/usr/bin/env python
"""
Extension to pythons `argparse` module.
"""
__author__ = "Alex Drlica-Wagner"
__email__ = "kadrlica@fnal.gov"
__version__ = "0.1.0"

import os,sys
import logging
import inspect

import argparse
try:
    # Use ConfigArgParse if available:
    # https://github.com/bw2/ConfigArgParse
    from configargparse import ArgumentParser
except ImportError:
    # Otherwise, use argparse
    from argparse import ArgumentParser

class RawDefaultsHelpFormatter(
        argparse.ArgumentDefaultsHelpFormatter,
        argparse.RawDescriptionHelpFormatter):
    """ 
    Help message formatter with raw discription and help defaults.
    """
    pass

class SpecialFormatter(logging.Formatter):
    """
    Class for overloading log formatting based on level.
    """
    # TODO: Send to stdout instead of stderr?
    FORMATS = {'DEFAULT'        : "%(levelname): %(message)s",
               logging.INFO     : "%(message)s"}
 
    def format(self, record):
        self._fmt = self.FORMATS.get(record.levelno, 
                                     self.FORMATS['DEFAULT'])
        return logging.Formatter.format(self, record)

class VerbosityAction(argparse._CountAction):
    """
    Class for setting logging level from verbosity.
    """
    sign = 'pos'
    help = 'modify output verbosity'

    def __init__(self,*args,**kwargs):
        kwargs.setdefault('help',self.help)
        kwargs.setdefault('default',argparse.SUPPRESS)
        kwargs.setdefault('default',0)
        super(VerbosityAction,self).__init__(*args,**kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        super(VerbosityAction,self).__call__(parser,namespace,values,option_string)
        sign = self.sign.lower()
        if sign in ('pos','plus','+'):
            level = logging.WARNING - 10*getattr(namespace, self.dest)
        elif sign in ('neg','minus','-'):
            level = logging.WARNING + 10*getattr(namespace, self.dest)
        else:
            msg = "Unrecognized verbosity sign: %s"%self.sign
            raise ValueError(msg)
        logging.getLogger().setLevel(level)

class IncreaseVerbosityAction(VerbosityAction):
    """
    Class for increasing output verbosity.
    """
    sign = 'pos'
    help = 'increase output verbosity'
    
class DecreaseVerbosityAction(VerbosityAction):
    """
    Class for decreasing output verbosity.
    """
    sign = 'neg'
    help = 'decrease output verbosity'

class DatetimeAction(argparse._StoreAction):
    """
    Class for setting logging level from verbosity.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        datetime = dateutil.parser.parse(values)
        setattr(namespace, self.dest, datetime)

class VersionAction(argparse._VersionAction):
    """ Add '%(prog)s' if not present.
    """
    def __init__(self,option_strings,version=None,**kwargs):
        if version and not version.startswith('%'):
            version = '%(prog)s '+version
        super(VersionAction, self).__init__(option_strings,version=version,**kwargs)

class ArgumentParserError(Exception):
    """An error raised by the parser."""
    pass

class ArgumentParser(ArgumentParser):
    """Subclass of argparse.ArgumentParser or
    configargparse.ArgumentParser (when available).

    """

    # Set the logging for output 
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(SpecialFormatter())
    logger.addHandler(handler)

    def __init__(self,*args,**kwargs):
        kwargs.setdefault('formatter_class',RawDefaultsHelpFormatter)
        super(ArgumentParser,self).__init__(*args,**kwargs)

        self.register('action','datetime',DatetimeAction)
        self.register('action','quiet'   ,DecreaseVerbosityAction)
        self.register('action','version' ,VersionAction)
        self.register('action','verbose' ,IncreaseVerbosityAction)

        group = self.add_mutually_exclusive_group()
        group.add_argument('-v','--verbose',action='verbose')
        group.add_argument('-q','--quiet',action='quiet')

        self.add_argument('-V','--version', action='version',version=__version__)
        #self.add_argument('--config', action='config')

    def remove_argument(self,option_string):
        """ Not very robust way to remove arguments """
        # TODO: subparsers?
        for i,action in enumerate(self._actions):
            if option_string in action.option_strings:
                self._handle_conflict_resolve(None, [(option_string,action)])
                #action.container._remove_action(action)

    def error(self, message):
        self.print_usage(sys.stderr)
        raise ArgumentParserError(message)

if __name__ == "__main__":
    parser = ArgumentParser()
    args = parser.parse_args()
    parser.print_help()

