# -*- coding: utf-8 -*-

"""Main module."""


def baby(name=None):
    """Say hello to the baby."""

    if name:
        msg = "Hello {} baby!".format(name)
    else:
        msg = "Hello baby!"

    return msg
