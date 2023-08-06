==========
redpackets
==========

RedPackets Split & Return split_list if succeed & Raise Exception if failed

Installation
============

::

    pip install redpackets


Usage
=====

::

    import redpackets

    # Redpackets Split
    redpackets.split_dollar(total, num, min=0.01)
    redpackets.split_cent(total, num, min=1)
    # cent=False equals split_dollar
    # cent=True equals split_cent
    redpackets.split(total, num, min=None, cent=False)

    # Exchange Cent & Dollar
    redpackets.cent(dollar, rate=100, cast_func=int)
    redpackets.dollar(cent, rate=100, cast_func=float)

    # Mul & Div
    redpackets.mul(multiplicand, multiplicator, cast_func=float)
    redpackets.div(dividend, divisor, cast_func=float)

