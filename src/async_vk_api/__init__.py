import logging

import asks

from .errors import ApiError
from .factories import make_api, make_session, make_throttler


asks.init('trio')

logging.getLogger(__name__).addHandler(logging.NullHandler())
