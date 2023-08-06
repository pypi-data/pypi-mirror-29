Ansible Dot-diff Library
========================

Nested structure diff library with dot-path notation for Ansible.

..  image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :alt: License: MIT
    :target: https://opensource.org/licenses/MIT

Description
-----------

This package is built to plug into Ansible's module_utils, which doesn't require
it to be installed on managed remote hosts, only the controller. It will be picked
up by Ansiballz, which zips a module's dependencies and ships it over SSH.
The library is kept small to keep the footprint down.

Usage
-----

By design, the algorithm will ignore any keys that are omitted on the right (the target),
to allow an API endpoint to choose plausible defaults. For example, an API client
implementing this library will diff the desired state with a JSON REST resource
to predict whether or not a REST call needs to occur for the user's changes to be applied.


    from ansible.module_utils.dotdiff import dotdiff

    orig = { 'one': 'one',
             'two': 'two' }

    dest = { 'one': 'another',
             'three': 'three' }

    dotdiff(orig, dest)


dotdiff() yields a list of DiffEntry objects:

    [one: "one" => "another", three: "<undefined>" => "three"]


Keys that would be added to the structure in this transaction have their values marked
as '<undefined>'.

Nested lists and dictionaries are supported at an arbitrary level and will be indicated
using dot-separated paths. Changing a list's member count will yield a DiffEntry indicating
a change in cardinality with a pound (#) sign.

    mylist.#: "3" => "4"

This visualization is inspired by Terraform.

License
-------

`MIT <https://github.com/Klarrio/ansible-dotdiff/blob/master/LICENSE>`_.
