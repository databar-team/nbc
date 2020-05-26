import os
import pytest

from concurrency.event_manager import EventManager

def test_event_manager_add_event():
    # given
    em = EventManager()

    # when
    for i in range(3):
        em.add_event("event_{}".format(i))

    # then
    assert 3 == len(em.events)
    assert em.events.get("event_0", False)
    assert em.events.get("event_1", False)
    assert em.events.get("event_2", False)
    assert False == em.events.get("event_3", False)

def test_event_manager_set():
    # given
    em = EventManager()

    for i in range(3):
        em.add_event("event_{}".format(i))

    # when
    em.set("event_0")
    em.set("event_2")

    # then
    assert em.events.get("event_0").is_set()
    assert em.events.get("event_2").is_set()
    assert False == em.events.get("event_1").is_set()

def test_event_manager_is_set():
    # given
    em1 = EventManager()
    em2 = EventManager()

    for i in range(3):
        em1.add_event("event_{}".format(i))
        em2.add_event("event_{}".format(i))

    # when
    em1.set("event_0")
    em1.set("event_1")
    em1.set("event_2")

    em2.set("event_0")
    em2.set("event_2")

    # then
    assert em1.is_set()
    assert False == em2.is_set()