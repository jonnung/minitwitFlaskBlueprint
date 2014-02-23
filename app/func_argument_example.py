# -*- coding: utf-8 -*-

def fn1(a, b, c):
    print a
    print b
    print c

def fn2(a=1, b=2, c=3):
    print a
    print b
    print c


def fn1_1(*args):
    print args[0]
    print args[1]
    print args[2]

def fn2_1(**kwargs):
    print kwargs['a']
    print kwargs['b']
    print kwargs['c']

def fn3(*args, **kwargs):
    print args
    print kwargs

def fn3_1(*args, **kwargs):
    fn1(*args)
    fn2(**kwargs)


fn1(1,1,1)
fn1_1(1,1,1)
fn2(a=1, b=2, c=3)
fn2_1(a=1, b=2, c=3)

fn3(1,2,3, z=1, y=2)
fn3_1(1,2,3, a=9, b=8)