# django-markers

A dynamic map marker generator using template images and arbitrary text.


## Why

Sometimes you need to use a lot of markers on a map, many of which are similar,
but slightly different, using text labels, or even different colours or
opacities.  This will do that for you.

Theoretically, you could also use it to caption memes, but I think there's
other stuff out there for that sort of thing.


## How

You can reference the markers in three ways: using a django template tag, via
URL parameters, or in Python, by using the `Marker` class.  The preferred
method is the template tag, and I don't recommend using direct URL requests,
since it requires a hit to your application server every time.

### Using a Template Tag

This will generate a media URL pointing to a newly-created marker based on a
`template.png`, with the text `42`, positioned `3` pixels right, and `3` pixels
down from the upper left corner of the template, with an opacity of `50%`, a
hue-shift of `105`, and using the hex colour `#333333` for the text.  All the
arguments, save for the first, are optional:

```django
{% load markers %}
{% marker 'path/to/template.png' text='42' text_x=3 text_y=3 opacity=0.5 hue=105 text_colour='333333' %}
```

Typically, you'll use this in your template to assign marker paths to some
javascript variables:

``django
<script>
  var marker1 = "{% marker 'path/to/template.png' text='1' %}";
  var marker2 = "{% marker 'path/to/template.png' text='3' hue=105 %}";
</script>
``

After you have the URLs in your Javascript, you can do whatever you like with
them, they're just URLs to existing static files.


### Using Direct Links

The same arguments passed to the template tag can be passed in a URL:

```
https://localhost:8000/markers/path/to/template.png?text=42&opacity=0.5&text_x=3&text_y=3&text_colour=333333&hue=105
```


### Using the Python Model

Marker generation is as easy as instantiating a model:

``python
from markers.models import Marker

mymarker = Marker(
    "path/to/template.png",
    text="42",
    opacity=0.5,
    text_x=3,
    text_y=3,
    text_colour="333333",
    hue=105
)
``


### The Templates

The template path you pass to `django-markers`, must be part of one of your
apps, and referenced as such.  So for example, if you have a template living in
`mapping/static/mapping/img/markers/mytemplate.png`, the argument you're
looking for is: `mapping/img/markers/mytemplate.png`.

If you're calling the URL directly, then you'll append this path to the URL
like so:

```
https://localhost:8000/markers/mapping/img/markers/mytemplate.png?hue=105&opacity=0.8
```


### A Note on Text Positioning

By default, we try to centre text along the x/y axis, so if that's your
intention, don't specify either.  Specifying an `x` value without a `y` one
will assume `y` to be centred and vice versa.


### A Note on Template Images

You can use whatever image you like for your templates, but since the
hue-shifting starts at red (0), and progresses through the spectrum to red
again at 360, you'd do well to use a redish image as your template.
Otherwise, requests that don't specify a `hue` will look out of step with
ones that have `hue` set to `1`.



## Installation

You can install it from pypi using `pip`:

```shell
$ pip install django-markers
```

Or you can install it from GitHub:

```shell
$ pip install git+https://github.com/danielquinn/django-markers.git#egg=django-markers
```


Then in your `settings.py`:

```python
INSTALLED_APPS = (
    ...
    "markers",
)
```

And if you want to make use of the direct URL requests, you'll need to add this
to your `urls.py`:

```python
url(r"^some/arbitrary/path/", include("markers.urls")),
```

So for example, you would have something like this in your `urls.py`:

```python
url(r"^mapping/markers/", include("markers.urls")),
```


### Requirements

We're doing image processing here, so `PIL` is required.  You should probably
use `Pillow` though, since that's what this was developed against.
Additionally, `numpy` is required to handle the hue-shifting.  Both will
install automatically if you follow the installation instructions above.

In addition to these Python dependencies, Django 1.6+ is required if you
intend to make use of the on-the-fly generation via calling a specific URL.


### Licensing

The whole project is licensed under the GPL-3, but the default font used is
licensed under Apache 2.0.