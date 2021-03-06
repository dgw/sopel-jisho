# sopel-jisho
Sopel module that provides search results from the Jisho Japanese/English dictionary

This module has alpha-level functionality. It can request and display most results, but
may not correctly deal with incomplete API responses (words that have no readings, for
example). That said, anything that doesn't behave as expected should be reported in the
module's [issue tracker](https://github.com/dgw/sopel-jisho/issues) if it isn't already
listed there (be sure to **also search closed issues!**).

Jisho's API is undocumented and subject to change, so there are sure to be edge cases
where the code receives something it doesn't expect. Some of these are handled. Others
aren't...yet. Report problematic queries to the issue tracker.

## Requirements
The Jisho module relies on the following Python modules:

* `requests` (should be in standard Python library)

## Usage
Commands & arguments:

* `.jisho <search query>` (also available as `.ji`)
  * `<search query>`: the keyword(s) to search for on Jisho

