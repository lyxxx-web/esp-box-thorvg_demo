# SPDX-FileCopyrightText: 2022-2023 Espressif Systems (Shanghai) CO LTD
#
# SPDX-License-Identifier: Apache-2.0

"""
This file is used in CI generate binary files for different kinds of apps
"""

import argparse
import sys
import os
import re
from pathlib import Path
from typing import List

from idf_build_apps import LOGGER, App, build_apps, find_apps, setup_logging

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
APPS_BUILD_PER_JOB = 30
IGNORE_WARNINGS = [
    r'1/2 app partitions are too small',
    r'\'bsp_button_get\' is deprecated: use espressif/button API instead',
    r'default on the choice symbol SEC_CERT_DAC_PROVIDER',
    r'the choice symbol SEC_CERT_DAC_PROVIDER',
    r'The legacy RMT driver is deprecated, please use driver/rmt_tx.h and/or driver/rmt_rx.h',
    r'warning: unknown kconfig symbol \'ESPTOOLPY_FLASHSIZE_DETECT\' assigned to*',
    r'warning: unknown kconfig symbol \'BTDM_CTRL_MODE_BLE_ONLY\' assigned to*',
    r'warning: unknown kconfig symbol \'IO_GLITCH_FILTER_TIME_MS\' assigned to*',
    r'warning: unknown kconfig symbol \'BSP_TOUCH_BUTTON\' assigned to*',
    r'warning: default value 0 on ESPNOW_OTA_SEND_FORWARD_TTL',
    r'WARNING: Unknown CPU family Generic',
]

def _get_idf_version():
    if os.environ.get('IDF_VERSION'):
        return os.environ.get('IDF_VERSION')
    version_path = os.path.join(os.environ['IDF_PATH'], 'tools/cmake/version.cmake')
    regex = re.compile(r'^\s*set\s*\(\s*IDF_VERSION_([A-Z]{5})\s+(\d+)')
    ver = {}
    with open(version_path) as f:
        for line in f:
            m = regex.match(line)
            if m:
                ver[m.group(1)] = m.group(2)
    return '{}.{}'.format(int(ver['MAJOR']), int(ver['MINOR']))

def get_cmake_apps(
    paths,
    target,
    config_rules_str,
    default_build_targets,
):  # type: (List[str], str, List[str]) -> List[App]
    idf_ver = _get_idf_version()
    apps = find_apps(
        paths,
        recursive=True,
        target=target,
        build_dir=f'{idf_ver}/build_@t_@w',
        config_rules_str=config_rules_str,
        build_log_path='build_log.txt',
        size_json_path='size.json',
        check_warnings=True,
        preserve=True,
        default_build_targets=default_build_targets,
        manifest_files=[
        ],
    )
    return apps


def main(args):  # type: (argparse.Namespace) -> None
    default_build_targets = args.default_build_targets.split(',') if args.default_build_targets else None
    apps = get_cmake_apps(args.paths, args.target, args.config, default_build_targets)
    if args.exclude_apps:
        apps_to_build = [app for app in apps if app.name not in args.exclude_apps]
    else:
        apps_to_build = apps[:]

    LOGGER.info('Found %d apps after filtering', len(apps_to_build))
    LOGGER.info(
        'Suggest setting the parallel count to %d for this build job',
        len(apps_to_build) // APPS_BUILD_PER_JOB + 1,
    )

    ret_code = build_apps(
        apps_to_build,
        parallel_count=args.parallel_count,
        parallel_index=args.parallel_index,
        dry_run=False,
        collect_size_info=args.collect_size_info,
        keep_going=True,
        ignore_warning_strs=IGNORE_WARNINGS,
        copy_sdkconfig=True,
    )

    sys.exit(ret_code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Build all the apps for different test types. Will auto remove those non-test apps binaries',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('paths', nargs='*', help='Paths to the apps to build.')
    parser.add_argument(
        '-t', '--target',
        default='all',
        help='Build apps for given target. could pass "all" to get apps for all targets',
    )
    parser.add_argument(
        '--config',
        default=['sdkconfig.ci=default', 'sdkconfig.ci.*=', '=default'],
        action='append',
        help='Adds configurations (sdkconfig file names) to build. This can either be '
        'FILENAME[=NAME] or FILEPATTERN. FILENAME is the name of the sdkconfig file, '
        'relative to the project directory, to be used. Optional NAME can be specified, '
        'which can be used as a name of this configuration. FILEPATTERN is the name of '
        'the sdkconfig file, relative to the project directory, with at most one wildcard. '
        'The part captured by the wildcard is used as the name of the configuration.',
    )
    parser.add_argument(
        '--parallel-count', default=1, type=int, help='Number of parallel build jobs.'
    )
    parser.add_argument(
        '--parallel-index',
        default=1,
        type=int,
        help='Index (1-based) of the job, out of the number specified by --parallel-count.',
    )
    parser.add_argument(
        '--collect-size-info',
        type=argparse.FileType('w'),
        help='If specified, the test case name and size info json will be written to this file',
    )
    parser.add_argument(
        '--exclude-apps',
        nargs='*',
        help='Exclude build apps',
    )
    parser.add_argument(
        '--default-build-targets',
        default=None,
        help='default build targets used in manifest files',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='count', default=0,
        help='Show verbose log message',
    )

    arguments = parser.parse_args()
    if not arguments.paths:
        arguments.paths = [PROJECT_ROOT]
    setup_logging(verbose=arguments.verbose)  # Info
    main(arguments)
