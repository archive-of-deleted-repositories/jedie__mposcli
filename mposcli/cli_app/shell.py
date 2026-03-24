import logging
import time
from typing import Annotated

import tyro
from cli_base.cli_tools.subprocess_utils import verbose_check_call
from cli_base.cli_tools.verbosity import setup_logging

from mposcli.cli_app import app
from mposcli.mpos_utils import get_mpos_path
from mposcli.shared_tyro import DEFAULT_VERBOSITY, TyroVerbosityArgType
from mposcli.tools import get_mpremote_bin
from mposcli.utilities.mpremote import start_mpremote_repl


logger = logging.getLogger(__name__)


@app.command
def shell(
    reset: Annotated[
        bool,
        tyro.conf.arg(help='Reset the device before starting the REPL?'),
    ] = False,
    verbosity: TyroVerbosityArgType = DEFAULT_VERBOSITY,
):
    """
    Start a REPL shell connected to the device using mpremote. Optional reset before starting the REPL.
    The goal it to try to get a REPL in a loop until it works.
    """
    setup_logging(verbosity=verbosity)
    mpos_path = get_mpos_path()
    mpremote_bin = get_mpremote_bin()

    if reset:
        time.sleep(1)
        verbose_check_call(
            mpremote_bin,
            'reset',
            verbose=True,
            cwd=mpos_path,
            text=None,
        )

    start_mpremote_repl()
