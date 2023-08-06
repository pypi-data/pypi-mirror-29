
from ._obj_from_dict import ObjFromDict

from .request_rotb_curves import RequestRotbCurves
from .response_rotb_curves import ResponseRotbCurves

from .request_rotb_compute_strategy_components import RequestRotbComputeStrategyComponents
from .response_rotb_compute_strategy_components import ResponseRotbComputeStrategyComponents
from .slice_rotb_compute_strategy_components import SliceRotbComputeStrategyComponents

from .request_rotb_compute_strategy import RequestRotbComputeStrategy
from .response_rotb_compute_strategy import ResponseRotbComputeStrategy
from .slice_rotb_compute_strategy import SliceRotbComputeStrategy

from .request_rotb_compute_strategy_prices import RequestRotbComputeStrategyPrices
from .response_rotb_compute_strategy_prices import ResponseRotbComputeStrategyPrices
from .slice_rotb_compute_strategy_prices import SliceRotbComputeStrategyPrices


dic_endpoint = {
    'v1_curves': {
        'request': RequestRotbCurves,
        'response': ResponseRotbCurves,
    },
    'v1_compute_strategy_components': {
        'request': RequestRotbComputeStrategyComponents,
        'response': ResponseRotbComputeStrategyComponents,
        'slice': SliceRotbComputeStrategyComponents,
    },
    'v1_compute_strategy': {
        'request': RequestRotbComputeStrategy,
        'response': ResponseRotbComputeStrategy,
        'slice': SliceRotbComputeStrategy,
    },
    'v1_compute_strategy_prices': {
        'request': RequestRotbComputeStrategyPrices,
        'response': ResponseRotbComputeStrategyPrices,
        'slice': SliceRotbComputeStrategyPrices,
    },
    # to add new endpoint here after creating the corresponding
    # Request Response and optionally Slice objects
}

endpoint = ObjFromDict(dic_endpoint)
