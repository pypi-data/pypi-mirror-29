
LoopyTimer
==========

Python looping timer. Forked from
`terryltang/pythonTimer <https://github.com/terryltang/pythonTimer>`__

Install
-------

::

    pip install loopytimer

Feature & Usage
---------------

-  Require Python standard library: **threading**

-  Call a function after a specified number of seconds:

::

        e.g.:
        from loopytimer import LoopyTimer

        timer = LoopyTimer(5.0, handler_func, args=[], kwargs={})
        timer.set_call_limits(5)    # timer will run eternally if you don't set a limit
        timer.start()
        timer.cancel()     # cancel the timer's action if it's still waiting, will also destroy timer instance

-  Timer handler take positional arguments and keyword arguments:

::

        e.g.: 
        timer = LoopyTimer(0.5, timer_handler, args=["Terry", "Tang"], kwargs={"city":"Houston", "state":"Texas"})

-  Cancel and destroy timer.

-  Add a customized logger function for timer handler.

-  Test cases included.

License
-------

MIT License

Copyright (c) 2018 Wavky Huang

See ->
`LICENSE <https://github.com/wavky/loopytimer/blob/master/LICENSE>`__


