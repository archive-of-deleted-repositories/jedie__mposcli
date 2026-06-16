import logging
from pathlib import Path
from typing import Annotated

import tyro
from cli_base.cli_tools.verbosity import setup_logging
from rich import print

from mposcli.cli_app import app
from mposcli.mpos_utils import get_mpos_path
from mposcli.shared_tyro import DEFAULT_VERBOSITY, TyroVerbosityArgType
from mposcli.tools import get_mpremote_bin
from mposcli.user_input import get_newest_files
from mposcli.utilities.mpremote import MpOsPathResolver, check_call_loop


logger = logging.getLogger(__name__)


@app.command
def run(
    local_path: Annotated[
        Path | None,
        tyro.conf.arg(
            help=(
                'Optional file path. If not provided, you can select from the list of the newest modified'
                ' files in internal_filesystem/lib/mpos.'
            )
        ),
    ] = None,
    /,
    new_file_limit: Annotated[
        int,
        tyro.conf.arg(help='How many of the newest files to show in the file chooser?'),
    ] = 10,
    verbosity: TyroVerbosityArgType = DEFAULT_VERBOSITY,
):
    """
    Run a script via "mpremote run": With optional file selection and retry loop.
    """
    setup_logging(verbosity=verbosity)

    mpos_path = get_mpos_path()
    resolver = MpOsPathResolver(mpos=mpos_path)

    mpremote_bin = get_mpremote_bin()

    print('\n')

    if not local_path:
        # Let's the user select from the list of the newest modified files in internal_filesystem/lib/mpos:
        local_path = get_newest_files(resolver.internal_fs, limit=new_file_limit)
        if not local_path:
            print('One file must be selected to run.')
            return

    print(f'Run: "{local_path}" ...')

    if not local_path.exists():
        print(f'[red]Error: The specified source path "{local_path}" does not exist.[/red]')
        return

    check_call_loop(
        popen_args=(mpremote_bin, 'run', local_path),
        max_try=10,
        wait_time=1,
        cwd=mpos_path,
        text=None,
    )
