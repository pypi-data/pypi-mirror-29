#!/usr/bin/env python3.6

"""The module meant to be run in order to start Astrality."""

import logging
import os
import signal
from typing import Set
import subprocess
import sys
import time

from astrality.config import user_configuration
from astrality.module import ModuleManager

logger = logging.getLogger('astrality')


def main(logging_level: str = 'INFO', test: bool = False):
    """
    Run the main process for Astrality.

    If test is set to True, then only one main loop is run as an integration
    test.
    """
    if 'ASTRALITY_LOGGING_LEVEL' in os.environ:
        # Override logging level if env variable is set
        logger.setLevel(os.environ['ASTRALITY_LOGGING_LEVEL'])
    else:
        # Set the logging level to the level passed in by bin/astrality cli
        logger.setLevel(logging_level)

    # Quit old astrality instances
    kill_old_astrality_processes()

    # How to quit this process
    def exit_handler(signal=None, frame=None) -> None:
        """Cleanup all temporary files and run module exit handlers."""

        # The temp directory is left alone, for two reasons:
        # 1: An empty directory uses neglible disk space.
        # 2: If this process is interrupted by another Astrality instance,
        #    we might experience race conditions when the exit handler deletes
        #    the temporary directory *after* the new Astrality instance creates it.

        logger.critical('Astrality was interrupted')
        logger.info('Cleaning up temporary files before exiting...')

        # Run all the module exit handlers
        module_manager.exit()

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

    # Some SIGINT signals are not properly interupted by python and converted
    # into KeyboardInterrupts, so we have to register a signal handler to
    # safeguard against such cases. This seems to be the case when conky is
    # launched as a subprocess, making it the process that receives the SIGINT
    # signal and not python. These signal handlers cause issues for \
    # NamedTemporaryFile.close() though, so they are only registrered when
    # we are not testing.
    if not test:
        signal.signal(signal.SIGINT, exit_handler)

        # Also catch kill-signkal from OS,
        # e.g. `kill $(pgrep -f "python astrality.py")`
        signal.signal(signal.SIGTERM, exit_handler)

    try:
        config = user_configuration()

        # Delay further actions if configuration says so
        startup_delay = float(config.get('settings/general', {}).get('startup_delay', '0'))
        time.sleep(startup_delay)

        module_manager = ModuleManager(config)
        module_manager.finish_tasks()

        # TODO: Implement startup delay config option

        while True:
            if module_manager.has_unfinished_tasks():
                # TODO: Log which new period which has been detected
                logger.info('New timer period detected.')
                module_manager.finish_tasks()
                logger.info(f'Period change routine finished.')

            if test:
                logger.debug('Main loop interupted since argument test=True.')
                return
            else:
                logger.info(
                    f'Waiting {module_manager.time_until_next_period()} '
                    'until next period change and ensuing update.'
                )
                time.sleep(
                    module_manager.time_until_next_period().total_seconds()
                )

    except KeyboardInterrupt:
        exit_handler()

def other_astrality_pids() -> Set[int]:
    """Return the process ids (PIDs) of any other Astrality instances."""

    # Get all processes instanciated from this file
    result = subprocess.Popen(
        ['pgrep', '-f', 'astrality'],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    pids = set(int(pid.strip()) for pid in result.stdout)

    # Return all the PIDs except for the PID of this process
    this_process_pid = os.getpid()
    return pids - set((this_process_pid,))


def kill_old_astrality_processes() -> None:
    """Kill all other instances of this script, to prevent duplicates."""

    pids = other_astrality_pids()
    failed_exits = 0
    for pid in pids:
        try:
            logger.info(f'Killing duplicate Astrality process with pid {pid}.')
            os.kill(pid, signal.SIGTERM)
        except OSError:
            logger.error(f'Could not kill old instance of astrality with pid {pid}.')
            logger.error('Continuing anyway...')
            failed_exits += 1

    while len(other_astrality_pids()) > failed_exits:
        # Wait for all the processes to exit properly
        time.sleep(0.2)


if __name__ == '__main__':
    main()
