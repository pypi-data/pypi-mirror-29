#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2018 TUNE, Inc. (http://www.tune.com)
#  @namespace requests_mv_integrations


def csv_skip_last_row(iterator):
    """Skip last CSV row.

    Args:
        iterator:

    Returns:

    """
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item
