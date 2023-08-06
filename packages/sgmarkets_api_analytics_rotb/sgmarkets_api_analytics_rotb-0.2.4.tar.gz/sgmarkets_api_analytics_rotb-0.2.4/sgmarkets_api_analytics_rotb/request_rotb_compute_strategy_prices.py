
from .request_rotb_compute_strategy_base import RequestRotbComputeStrategyBase

LIMIT_SPLIT_REQUEST = 500


class RequestRotbComputeStrategyPrices(RequestRotbComputeStrategyBase):
    """
    """

    def __init__(self,
                 dic=None,
                 date_fallback_next=True,
                 limit_split=LIMIT_SPLIT_REQUEST):
        """
        """
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/rotb',
                   'endpoint': '/v1/compute-strategy/prices'}
        super().__init__(dic,
                         date_fallback_next,
                         limit_split,
                         dic_url)
