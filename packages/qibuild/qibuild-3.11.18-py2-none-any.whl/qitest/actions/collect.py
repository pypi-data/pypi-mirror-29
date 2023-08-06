# Copyright (c) 2012-2018 SoftBank Robotics. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the COPYING file.
""" Collect all python test in worktree """

from qisys import ui
import qipy.parsers
import qibuild.parsers
from qitest.collector import PythonTestCollector


def configure_parser(parser):
    qibuild.parsers.cmake_build_parser(parser)


def do(args):
    python_worktree = qipy.parsers.get_python_worktree(args)
    ui.info(ui.green, "python projects in:", ui.blue, python_worktree.root)
    collector = PythonTestCollector(python_worktree)
    collector.collect()
