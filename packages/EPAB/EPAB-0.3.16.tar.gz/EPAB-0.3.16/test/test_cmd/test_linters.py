# coding=utf-8

import itertools

import pytest
from pathlib import Path
from mockito import mock, verify, verifyNoMoreInteractions, when, verifyStubbedInvocationsAreUsed

import epab.utils
from epab.core import CONFIG, CTX
from epab.linters import _flake8, _sort, _lint, _pep8, _pylint, _safety


@pytest.fixture(autouse=True, name='repo')
def _all():
    repo = mock(spec=epab.utils.Repo)
    CTX.repo = repo
    yield repo


@pytest.mark.parametrize(
    'amend_stage',
    itertools.product([False, True], repeat=2),
)
def test_lint(amend_stage):
    amend, stage = amend_stage
    context = mock()
    _lint._lint(context, amend, stage)
    verify(context).invoke(_safety.safety)
    verify(context).invoke(_pylint.pylint)
    verify(context).invoke(_flake8.flake8)
    verify(context).invoke(_sort.sort, amend=amend, stage=stage)
    verify(context).invoke(_pep8.pep8, amend=amend, stage=stage)
    verifyNoMoreInteractions(context)


@pytest.mark.parametrize(
    'amend_stage',
    itertools.product([False, True], repeat=2),
)
def test_lint_appveyor(amend_stage):
    amend, stage = amend_stage
    CTX.appveyor = True
    context = mock()
    _lint._lint(context, amend, stage)
    verify(context).invoke(_safety.safety)
    verify(context).invoke(_pylint.pylint)
    verify(context).invoke(_flake8.flake8)
    verify(context).invoke(_pep8.pep8, amend=amend, stage=stage)
    verifyNoMoreInteractions(context)


def test_pep8():
    with when(epab.utils).run(f'autopep8 -r --in-place --max-line-length {CONFIG.lint__line_length} .', mute=True):
        _pep8._pep8()
        verify(epab.utils).run(...)


def test_pep8_amend():
    with when(CTX.repo).amend_commit(append_to_msg='pep8 [auto]'):
        CTX.run_once = {}
        _pep8._pep8(amend=True)
        verify(CTX.repo).amend_commit(...)


def test_pep8_stage():
    with when(epab.utils).run(f'autopep8 -r --in-place --max-line-length {CONFIG.lint__line_length} .', mute=True):
        with when(CTX.repo).stage_all():
            CTX.run_once = {}
            _pep8._pep8(stage=True)
            verify(CTX.repo).stage_all(...)


def test_isort():
    test_file = Path('./test.py')
    test_file.touch()
    with when(_sort.isort).SortImports(file_path=test_file.absolute(), **_sort.SETTINGS):
        _sort._sort()
        verifyStubbedInvocationsAreUsed()


def test_isort_amend():
    with when(epab.utils).run(f'isort -rc -w {CONFIG.lint__line_length} .', mute=True):
        with when(CTX.repo).amend_commit(append_to_msg='sorting imports [auto]'):
            _sort._sort(amend=True)
            verify(CTX.repo).amend_commit(...)


def test_isort_stage():
    with when(epab.utils).run(f'isort -rc -w {CONFIG.lint__line_length} .', mute=True):
        with when(CTX.repo).stage_all():
            _sort._sort(stage=True)
            verify(CTX.repo).stage_all(...)


def test_flake8():
    base_cmd = ' '.join((_flake8.IGNORE, _flake8.MAX_LINE_LENGTH, _flake8.EXCLUDE, _flake8.MAX_COMPLEXITY))
    with when(epab.utils).run(f'flake8 {base_cmd}', mute=True):
        _flake8._flake8()
        verify(epab.utils).run(...)


def test_safety():
    with when(epab.utils).run('safety check --bare', mute=True):
        _safety._safety()
        verify(epab.utils).run(...)


@pytest.mark.parametrize(
    'params,cmd',
    [
        ((None, True), 'pylint ./test --reports=y'),
        ((None, False), 'pylint ./test --reports=n'),
        (('src', False), 'pylint src --reports=n'),
    ]
)
def test_pylint(params, cmd):
    CONFIG.load()
    CONFIG.package = 'test'
    with when(epab.utils).run(f'{cmd} {_pylint.BASE_CMD}', mute=True):
        _pylint._pylint(*params)
        verify(epab.utils).run(...)
