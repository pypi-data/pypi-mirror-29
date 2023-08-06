#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2018 TUNE, Inc. (http://www.tune.com)
#  @namespace requests_mv_integrations

from .base import TuneRequestBaseError

from .custom import (
    TuneRequestError,
    TuneRequestClientError,
    TuneRequestServiceError,
    TuneRequestModuleError,
    TuneRequestValueError,
    TuneRequestAuthenticationError,
)
