* argdispatch 1.0.0 (2018-03-07)

    * Fix examples in README and documentation.
    * Drop python3.4 support
    * Minor code and documentation improvements.

    -- Louis Paternault <spalax+python@gresille.org>

* argdispatch 0.2.0 (2017-04-28)

    * Add python3.6 support.
    * Help message are no longer searched in `__main__` modules and in modules
      that are not packages. Closes #2.

        This adds a (minor) backward incompatibility, since some help messages
        are no longer searched in the same module they were searched before (or a
        no longer searched at all). However, this was necessary because it fixes
        a bad design. For instance, searching a help message in the docstring of
        a `__main__` package means importing it to access the docstring, and
        (maybe) importing it again to run it. This is discouraged, and displayed
        the warning (described in #2).

    -- Louis Paternault <spalax+python@gresille.org>

* argdispatch 0.1.1 (2016-05-21)

    * Fix default values for `ondouble` and `onerror` arguments.
    * Small internal and documentation fixes.

    -- Louis Paternault <spalax+python@gresille.org>

* argdispatch 0.1.0 (2016-04-14)

    * No change compared to beta version.

    -- Louis Paternault <spalax+python@gresille.org>

* argdispatch 0.1.0-beta1 (2016-04-12)

    * Initial release

    -- Louis Paternault <spalax+python@gresille.org>
