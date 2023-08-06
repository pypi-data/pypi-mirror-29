#!/usr/bin/env python
# -*- coding:utf-8 -*-


def init(driver="MySQL", **kwargs):
    if driver.lower() == "mysql":
        from .MySQL import ChainDB
        return ChainDB(**kwargs)
