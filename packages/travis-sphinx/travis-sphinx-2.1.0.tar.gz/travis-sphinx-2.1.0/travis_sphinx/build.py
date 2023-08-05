# -*- coding: utf-8 -*-
import logging

import click
import sphinx

from .main import main

_logger = logging.getLogger(__name__)


@click.command(
    help="Build sphinx documentation."
)
@click.option(
    '-s', '--source',
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    help='Source directory of sphinx docs',
    default='docs/source',
    show_default=True
)
@click.option(
    '-n', '--nowarn',
    type=click.BOOL,
    is_flag=True,
    help='Do not error on warnings',
)
@click.pass_context
def build(ctx, source, nowarn):
    """
    Build documentation from ``source``, placing built files in
    ``target``.
    """
    _logger.info('building documentation')
    outdir = ctx.obj['outdir']

    try:
        # Location from Sphinx 1.7 on
        sphinx_build = sphinx.cmd.build.build_main
        # args have to be specified this way for 1.7+, otherwise one gets
        # "Builder name  html not registered or available through entry point"
        args = ['-b', 'html']
    except AttributeError:
        # Old location
        sphinx_build = sphinx.build_main
        args = ['-b html']

    if not nowarn:
        args.append('-W')
    if sphinx_build(args + [source, outdir]):
        raise click.ClickException("Error building sphinx doc")


main.add_command(build)
