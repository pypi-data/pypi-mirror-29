**Lord of the Config** is a super-simple YAML-based configuration system. No
more meaningless key-checking or file creation. LOTConfig makes it easy to
create, manage, and write configurations.

Repository: https://bitbucket.org/bear_belly/lord_of_the_config

## Examples

Here are some quick-and-dirty examples for how the engine works::

    Python 3.6.3 (default, Oct  3 2017, 21:45:48)
    [GCC 7.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from lotconfig import Config
    >>> config = Config.load_or_create("sample.yaml")
    >>> config['basic/thing']
        'my_value'

## Loading a config

Configs are loaded from YAML files. To load a config use the `Config.load`,
method or--better yet--the `Config.load_or_create()` method for fool-proof
config loading. This will create the file if it doesn't exist.

## Accessing config values

To access configuration values, you can either use `config.get()` or
dict-like access:

    # This will return "default_value" if nothing is set in '/path/to/param'
    config.get('path/to/param', 'default_value')
    # This will just return `None` if nothing is set in '/path/to/param'
    config['/path/to/param']

You can use typical dict functions, too, like `in`.

## Setting Configuration Values

Woah, there tiger! Unfortunately this isn't implemented yet. Since LOTConfig
implements advanced features (see below), setting a configruation value is
pretty intensive.

Hopefully it'll happen in the future.

In the meantime you'll be greeted with an Exception if you try to do this.

## Writing a configuration

To write a configuration, call `config.write()` or `config.write_stream()`.

## Advanced features

### Modes

**Modes** are special keywords in the yaml configuration.

There's a default keyword you can specify at the beginning of the file
to specify a mode. For example::

    mode: development

This mode can be used throughout the file to specify different
environments. For the mode value, prefix it with '@' (**and make sure
to surround it with quotes, since YAML doesn't like '@' for keys**).
For example:

    server:
        '@development':
            host: localhost
            port: 5000
        '@production':
            host: example.com
            port: 5000

This way, whenever ``mode`` is ``'production'``, you can refer ``server``
will automatically refer to ``{host: "example.com", "port": 5000}``, and if
mode is set to ``developemnt``, then ``server`` will refer to
``{host: "localhost", "port": 5000}``.

**IMPORTANT.** These mode keys are essentially invisible. You can't
force the configuation to read ``config['server/@development/host']``.

So if mode is ``production`` ``config['server/host']`` is ``example.com``.
If mode is ``development`` ``config['server/host']`` is ``localhost``.

### References

Don't repeat yourself. You can refer to another value within the config
using a key reference. Key references are strings that refer to other
config values.

References are preceded with a tilde (``~``).

Consider the following example:

    database:
        home: ~server1
        remote: ~server2
    hardware:
        servers:
            server1: 192.168.0.1
            server2: 192.168.0.2

This would result in the following configuration:

    >> config['database/home']
      '192.168.0.1'
    >> config['database/remote']
      '192.16.0.2'

See? References help you to reduce the amount you have to type. You can even
use it for complex configurations:

    letter_a:
        category_a: ~cat_a
        category_b: ~cat_b
    letter_b:
        cat_a:
            item_a: 1
            item_b: false
        cat_b:
            item_a: 19
            item_b: 20

This would result in the following configuration:

    >> config['letter_a/category_a']
      {'item_a': 1, 'item_b': false}

### evals

Evals are probably the most powerful fo the bunch. They evaluate raw Python
code. **As such, use LOTConfig only on configuration files you trust**. In
future versions a paramter may be passed to turn on evaluations.

Evals begin with the keyword `eval>>`. The result is *always* a raw string.
For example:

    key: eval>> 1+2  # results in `config['key']` -> '3'

Two modules are available to be evaluated: `os` and `env`.

    key: eval>> os.environ['DISPLAY']
    # results in `config['key']` -> ':0'

Home-page: UNKNOWN
Author: Jordan Hewitt
Author-email: jordan.h@startmail.com
License: GPLv3
Description-Content-Type: UNKNOWN
Description: UNKNOWN
Platform: UNKNOWN
