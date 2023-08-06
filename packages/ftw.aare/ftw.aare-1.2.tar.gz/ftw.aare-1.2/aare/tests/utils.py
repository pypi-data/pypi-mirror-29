import sys
from contextlib import contextmanager
from json import loads

from path import Path

from aare import aare

ASSETS = Path(__file__).joinpath('..', 'assets').abspath()

@contextmanager
def capture_streams(stdout=None, stderr=None):
    ori_stdout = sys.stdout
    ori_stderr = sys.stderr

    if stdout is not None:
        sys.stdout = stdout
    if stderr is not None:
        sys.stderr = stderr

    try:
        yield
    finally:
        if stdout is not None:
            sys.stdout = ori_stdout
        if stderr is not None:
            sys.stderr = ori_stderr


@contextmanager
def cli_arguments(args):
    before = sys.argv
    sys.argv = [before[0]] + args.split(" ")
    try:
        yield
    finally:
        sys.argv = before


class SessionMock:
    def __init__(self):
        self.requests = []
        self.expected = {}

    def get(self, url, **kwargs):
        kwargs['url'] = url
        self.requests.append(kwargs)
        return ResponseStub(self.expected[url])

    def expect_get(self, url, asset):
        self.expected[url] = loads((ASSETS / asset).bytes())
        return self

    def __enter__(self):
        self.before = aare.session
        aare.session = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        aare.session = self.before


class ResponseStub:
    def __init__(self, result):
        self.result = result

    def json(self):
        return self.result

