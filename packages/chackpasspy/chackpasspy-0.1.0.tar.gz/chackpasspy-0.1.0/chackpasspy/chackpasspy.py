# -*- coding: utf-8 -*-

"""Main module."""

def checkio(data):
    """Check string input for password uses"""
    mini = False
    may = False
    num = False
    res = False

    if(len(data)>=10):

        for x in data:

            if(x.islower()):
                mini = True
            if(x.isupper()):
                may = True
            if(x.isdigit()):
                num = True
        if(mini and may and num):
            res = True

        else:
            res = False

    return res
