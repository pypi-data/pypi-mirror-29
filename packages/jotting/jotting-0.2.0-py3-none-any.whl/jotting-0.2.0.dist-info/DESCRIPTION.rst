
Jotting
-------

Logs that explain when, where, and why things happen.

``jotting`` is a log system for Python that can be used to record the causal
history of an asynchronous or distributed system. These histories are composed
of actions which, once "started", will begin "working", potentially spawn other
actions, and eventually end as a "success" or "failure". In the end you're left
with a breadcrumb trail of information that you can use to squash bugs with
minimal boilerplate.

Jotting was heavily inspired by ``eliot`` (https://eliot.readthedocs.io/).


