#!/usr/bin/env python
"""
Test functions for adwparse module
"""
__author__ = "Alex Drlica-Wagner"
import os
import adwparse
import logging

def test_verbosity():
    #logger = logging.getLogger()
    logging.getLogger().setLevel(logging.WARNING)

    parser = adwparse.ArgumentParser()

    args = parser.parse_args([])
    assert logging.getLogger().getEffectiveLevel() == logging.WARNING

    args = parser.parse_args('-v'.split())
    assert logging.getLogger().getEffectiveLevel() == logging.INFO

    args = parser.parse_args('-vv'.split())
    assert logging.getLogger().getEffectiveLevel() == logging.DEBUG

    args = parser.parse_args('-q'.split())
    assert logging.getLogger().getEffectiveLevel() == logging.ERROR

    args = parser.parse_args('-qq'.split())
    assert logging.getLogger().getEffectiveLevel() == logging.CRITICAL

    args = parser.parse_args('-q -q'.split())
    assert logging.getLogger().getEffectiveLevel() == logging.CRITICAL

    args = parser.parse_args('-qqqqq'.split())
    assert logging.getLogger().getEffectiveLevel() > logging.CRITICAL

    try: args = parser.parse_args('-vv -qq'.split())
    except adwparse.ArgumentParserError: pass
    else: raise AssertionError
    
if __name__ == "__main__":
    test_verbosity()
