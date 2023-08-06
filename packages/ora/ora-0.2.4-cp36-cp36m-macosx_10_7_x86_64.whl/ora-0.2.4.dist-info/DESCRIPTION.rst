
Ora is a coherent and high-perforamance C++ and Python 3 library for times,
dates, time zones, and related concepts.  The central concept is a
location-independent instant of time.  Local date and time of day
representations are derived from this, using the (included) zoneinfo database.
Multiple resolutions are provided for all time types.

.. code:: py

    >>> import ora
    >>> time = ora.now()
    >>> print(time)
    2017-12-26T03:47:36.41359399Z
    >>> tz = ora.TimeZone("US/Eastern")
    >>> (time @ tz).date
    Date(2017, Dec, 25)



