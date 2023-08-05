# -*- coding: utf-8 -*-

import gc
import logging
import re
import resource
import time

import pytest

from django.contrib.auth import get_user_model

from dj.debug import (
    debug_sql, log_new_queries, log_timing, memusage, timings,
    trace_debug)

logger = logging.getLogger(__name__)


def test_debug_timing_logger(caplog):
    caplog.set_level(logging.DEBUG)
    start = time.time()

    log_timing(start, debug_logger=logger)
    message = caplog.records[0].msg
    assert message.startswith("Timing: ")
    assert message.endswith(" seconds")

    log_timing(start, timed="Foo", debug_logger=logger)
    message = caplog.records[1].msg
    assert message.startswith("Timing for Foo: ")
    assert message.endswith(" seconds")


def test_debug_timing_contextmanager(caplog):
    caplog.set_level(logging.DEBUG)
    with timings(debug_logger=logger):
        pass
    message = caplog.records[0].msg
    assert message.startswith("Timing: ")
    assert message.endswith(" seconds")

    with timings(timed="Foo", debug_logger=logger):
        pass
    message = caplog.records[1].msg
    assert message.startswith("Timing for Foo: ")
    assert message.endswith(" seconds")


@pytest.mark.django_db
def test_debug_sql_logger(caplog, settings):
    from django.db import connection

    caplog.set_level(logging.DEBUG)

    settings.DEBUG = True

    queries = len(connection.queries)

    log_new_queries(queries, debug_logger=logger)
    assert len(caplog.records) == 2
    assert caplog.records[0].message == "total db calls: 0"
    assert caplog.records[1].message == "total db time: 0"

    # trigger some sql and log
    get_user_model().objects.count()

    log_new_queries(queries, debug_logger=logger)

    timing = caplog.records[2].msg
    sql = caplog.records[3].message
    assert caplog.records[4].message == "total db calls: 1"

    # match the timing, sql
    assert re.match("^\d+?\.\d+?$", timing)
    assert "SELECT COUNT" in sql
    assert "auth_user" in sql


@pytest.mark.django_db
def test_debug_sql_contextmanager(caplog, settings):
    caplog.set_level(logging.DEBUG)

    with debug_sql(debug_logger=logger):
        pass
    assert len(caplog.records) == 2
    assert caplog.records[0].message == "total db calls: 0"
    assert caplog.records[1].message == "total db time: 0"

    # should work even when debug is False
    settings.DEBUG = False

    # trigger some sql and log
    with debug_sql(debug_logger=logger):
        get_user_model().objects.count()

    timing = caplog.records[2].message
    sql = caplog.records[3].message
    assert caplog.records[4].message == "total db calls: 1"

    # match the timing, sql
    assert re.match("^\d+?\.\d+?$", timing)
    assert "SELECT COUNT" in sql
    assert "auth_user" in sql

    # settings shold be correct
    assert settings.DEBUG is False


def test_debug_trace(caplog, settings):

    with pytest.raises(NameError):
        _trace  # noqa: F821

    trace_debug()
    assert _trace  # noqa: F821

    with pytest.raises(NameError):
        _t  # noqa: F821

    trace_debug("_t")
    assert _t  # noqa: F821

    def _test_debug():
        assert _trace.debug  # noqa: F821

    def _test_no_debug():
        assert not _trace.debug  # noqa: F821

    def _test_trace(*args, **kwargs):
        _trace(*args, **kwargs)  # noqa: F821

    _test_no_debug()
    _trace.debug = True  # noqa: F821
    _test_debug()
    _trace.debug = False  # noqa: F821
    _test_no_debug()

    _trace("called", "here")  # noqa: F821
    called = list(_trace)  # noqa: F821

    # trace was emptied
    assert not list(_trace)  # noqa: F821
    assert called[0].stack[1] == __file__
    assert called[0].stack[3] == "test_debug_trace"
    assert called[0].args == ("called", "here")
    assert called[0].kwargs == {}
    assert (
        str(called[0])
        == ", ".join(
            [called[0].stack[1],
             str(called[0].stack[2]),
             called[0].stack[3],
             str(called[0].args),
             str(called[0].kwargs)]))

    _test_trace("foo0", "bar0", baz=0)
    _trace("foo1", "bar1", baz=1)  # noqa: F821
    _test_trace("foo2", "bar2", baz=2)

    asstring = str(_trace)  # noqa: F821
    called = list(_trace)  # noqa: F821
    for i in range(0, 2):
        assert called[i].stack[1] == __file__
        assert called[i].args == (("foo%s" % i), ("bar%s" % i))
        assert called[i].kwargs == dict(baz=i)
    assert called[0].stack[3] == "_test_trace"
    assert called[1].stack[3] == "test_debug_trace"
    assert called[2].stack[3] == "_test_trace"
    assert asstring == "\n".join(str(item) for item in called)


def test_debug_memusage():
    """Site wide update_stores"""
    gc.collect()

    initial = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    with memusage() as usage:
        foo = "BAR"

    assert foo
    assert usage["initial"] >= initial
    assert usage["after"] >= initial
    assert "used" in usage
