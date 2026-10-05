# sopel-jisho

Sopel plugin to search Jisho.org, a Japanese/English dictionary.

## Installing

Releases are hosted on PyPI, so after installing Sopel, all you need is `pip`:

```shell
$ pip install sopel-jisho
```

### Requirements

`sopel-jisho` requires Sopel 7.1+ and `requests`.

## Usage
Commands & arguments:

* `.jisho <search query>` (also available as `.ji`)
  * `<search query>`: the keyword(s) to search for on Jisho

## Notes

The plugin is more or less stable. In testing, this version has not yet failed
to output definitions when available.

However, Jisho's API is undocumented and subject to change, so there are sure to
be edge cases where the code receives something it doesn't expect. Some of these
are handled. Others aren't…yet. Check the [issue tracker][] if you run into
anything that doesn't seem to work correctly, and create a report if needed.

[issue tracker]: https://github.com/dgw/sopel-jisho/issues
