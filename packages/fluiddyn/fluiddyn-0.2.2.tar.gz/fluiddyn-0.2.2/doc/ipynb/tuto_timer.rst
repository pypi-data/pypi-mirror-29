
Timer
=====

This notebook demonstrates how the classes :class:`fluiddyn.util.timer.Timer` and :class:`fluiddyn.util.timer.TimerIrregular` can be used to loop with controled times.

We import the 2 classes:

.. code:: ipython3

    from fluiddyn.util.timer import Timer, TimerIrregular

Let's first use the regular timer:

.. code:: ipython3

    timer = Timer(0.02)
    
    for i in range(10):
        print(f'before tick {i}... ', end='')
        timer.wait_tick()
        print("It's time to tick", i)



.. parsed-literal::

    before tick 0... It's time to tick 0
    before tick 1... It's time to tick 1
    before tick 2... It's time to tick 2
    before tick 3... It's time to tick 3
    before tick 4... It's time to tick 4
    before tick 5... It's time to tick 5
    before tick 6... It's time to tick 6
    before tick 7... It's time to tick 7
    before tick 8... It's time to tick 8
    before tick 9... It's time to tick 9


Ok. This is the simplest way to use it. But we don't see when the timer
ticked. Let's print these times:

.. code:: ipython3

    timer = Timer(0.02)
    
    for i in range(10):
        print(f'before tick {i}... ', end='')
        t_tick = timer.wait_tick()
        print("It's time to tick", i, f'(t = {t_tick:.4f} s)')


.. parsed-literal::

    before tick 0... It's time to tick 0 (t = 0.0202 s)
    before tick 1... It's time to tick 1 (t = 0.0402 s)
    before tick 2... It's time to tick 2 (t = 0.0601 s)
    before tick 3... It's time to tick 3 (t = 0.0802 s)
    before tick 4... It's time to tick 4 (t = 0.1001 s)
    before tick 5... It's time to tick 5 (t = 0.1202 s)
    before tick 6... It's time to tick 6 (t = 0.1402 s)
    before tick 7... It's time to tick 7 (t = 0.1602 s)
    before tick 8... It's time to tick 8 (t = 0.1802 s)
    before tick 9... It's time to tick 9 (t = 0.2002 s)


Now, we see that it's ticking regularly... and it seems with a quite
good accuracy for many needs.

But what can we do if we need irregular steps between the ticks?

.. code:: ipython3

    times = [0, 0.05, 0.07, 0.1]
    timer = TimerIrregular(times)
    
    for i in range(len(times)-1):
        print(f'before tick {i}... ', end='')
        t_tick = timer.wait_tick()
        print("It's time to tick", i, f'(t = {t_tick:.4f} s)')


.. parsed-literal::

    before tick 0... It's time to tick 0 (t = 0.0502 s)
    before tick 1... It's time to tick 1 (t = 0.0702 s)
    before tick 2... It's time to tick 2 (t = 0.1002 s)

