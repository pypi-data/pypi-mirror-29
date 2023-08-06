""" Set the configuration to be used when building host tools"""

import qisys.parsers
import qibuild.config


def configure_parser(parser):
    """ Configure parser for this action """
    qisys.parsers.default_parser(parser)
    parser.add_argument("name")


def do(args):
    """ Main entry point """
    name = args.name
    qibuild_cfg = qibuild.config.QiBuildConfig()
    qibuild_cfg.read(create_if_missing=True)
    qibuild_cfg.set_host_config(name)
    qibuild_cfg.write()
