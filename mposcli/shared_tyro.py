from typing import Annotated

import tyro
from tyro.conf import UseCounterAction


DEFAULT_VERBOSITY = 1  # Display warnings by default

# https://brentyi.github.io/tyro/examples/04_additional/12_counters/
TyroVerbosityArgType = Annotated[
    UseCounterAction[int],
    tyro.conf.arg(
        aliases=['-v'],
        help='Verbosity level; e.g.: -v, -vv, -vvv, etc.',
        default=DEFAULT_VERBOSITY,
    ),
]
