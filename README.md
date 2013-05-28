# django-markers

A dynamic map marker generator using template images and arbitrary text.


## Why

Sometimes you need to use a lot of markers on a map, many of which are similar,
but slightly different, using text labels, or even different colours or
opacities.  This will do that for you.

Theoretically, you could also use it to caption memes, but I think there's
other stuff out there for that sort of thing.


## How

You can reference the markers in two ways: using a django template tag, or
directly via URL parameters.  The former is preferred, and the latter is not
recommended, since it requires a hit to your application server every time,
but both will work anyway.

### Using a Template Tag:

This will generate a media URL pointing to a newly-created marker based on a
`template.png`, with the text `42`, positioned `3` pixels right, and `3` pixels
down from the upper left corner of the template, with an opacity of 50%, a
hue-shift of 105, and using the hex colour `#333333` for the text.  All of the
arguments, save for the first, are optional:

    {% marker 'path/to/template.png' text='42' text_x=3 text_y=3 opacity=0.5 hue=105 text_colour='333333' %}

Typically, you'll use this in your template to assign marker paths to some
javascript variables:

    <script>
      var marker1 = "{% marker 'path/to/template.png' text='1' %}";
      var marker2 = "{% marker 'path/to/template.png' text='3' hue=105 %}";
    </script>

After you have the URLs in your Javascript, you can do whatever you like with
them, they're just URLs to existing static files.


### Using Direct Links

The same arguments passed to the template tag can be passed in a URL:

    https://localhost:8000/markers/path/to/template.png?text=42&opacity=0.5&text_x=3&text_y=3&text_colour=333333&hue=105


## Installation

You can install it from GitHub using `pip`:

    $ pip install git+https://github.com/danielquinn/django-markers.git#egg=django-markers

In your `settings.py`:

    INSTALLED_APPS = (
        ...
        "markers",
    )

And if you want to make use of the direct URL requests, you'll need to add this
to your `urls.py`:

    url(r"^some/arbitrary/path/", include("markers.urls")),

So for example, you would have something like this in your `urls.py`:

    url(r"^mapping/markers/", include("markers.urls")),


### The Templates

The template path you pass to `django-markers`, either as a URL argument or in
a template tag must be part of one of your apps, and referenced as such.  So
for example, if you have a template living in
`mapping/static/mapping/img/markers/mytemplate.png`, the argument you're
looking for is: `mapping/img/markers/mytemplate.png`.


## Licensing

The whole project is licesned under the GPL-3, but the default font used is
licensed under Apache 2.0.  Both licenses are available under `COPYING/`.
