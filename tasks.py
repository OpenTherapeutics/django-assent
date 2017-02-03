# -*- coding: utf-8 -*-
import os
import sys
from invoke import task

BUILDDIR = "build"
PROJECT = "assent"

@task
def clean(ctx):
    """Removes all the cache files"""
    ctx.run("find . -type d -name __pycache__ | xargs rm -rf")
    ctx.run('rm -rf ./.cache')
    builddir = os.path.join(__file__, BUILDDIR)
    if os.path.exists(builddir):
        print('Removing builddir {}'.format(builddir))
        ctx.run('rm -rf {}'.format(builddir))


@task
def install(ctx):
    """Installs the libraries required to run the application"""
    ctx.run("pip install -U pip")
    ctx.run("pip install -qr requirements/base.txt")


@task(install)
def develop(ctx):
    """Installs all the libraries used for development"""
    ctx.run("pip install -qr requirements/dev.txt")


@task
def checks(ctx):
    """Runs pep8/flake8 checks on the code"""
    excl = "--exclude='build/,*migrations/*'"
    ctx.run("pep8 {} .".format(excl))
    ctx.run("flake8 {} .".format(excl))


@task
def test(ctx):
    """Runs the tests"""
    ctx.run(
        'PYTHONPATH=`pwd` '
        "py.test --cov-config .coveragerc --cov-report html --cov-report term --cov={}".format(
            PROJECT
        ),
        pty=True
    )

    if sys.platform == 'darwin':
        ctx.run('open {}/coverage/index.html'.format(BUILDDIR))

