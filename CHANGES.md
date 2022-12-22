# Changes

## 1.4.0

Fixed a fun XSS problem where the markers were rendering just fine, but the
*error message* displayed in the event of a 4xx error could include malicious
code.


## 1.3.2

Bugfix: Encode the template & hue before hashing
[#2](https://github.com/danielquinn/django-markers/pull/2).
Thanks to [Robert Kisteleki](https://github.com/robert-kisteleki) for this
one.


## 1.3.1

Bugfix: Encode the duplication-check before hashing
[#1](https://github.com/danielquinn/django-markers/pull/1/).  Thanks to
[Viktor Naumov](https://github.com/the-vty) for this one.


## 1.3.0

Added Python 3 support.

