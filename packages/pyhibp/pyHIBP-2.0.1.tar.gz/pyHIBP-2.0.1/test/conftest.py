import pytest

import pyHIBP


@pytest.fixture(autouse=True)
def dev_user_agent(monkeypatch):
    monkeypatch.setattr(pyHIBP, 'pyHIBP_USERAGENT', "pyHIBP: A Python Interface to the Public HIBP API <testing suite>")
