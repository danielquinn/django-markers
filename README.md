# django-markers

A dynamic map marker generator using template images and arbitrary text.


## Why

Sometimes you need to use a lot of markers on a map, many of which are similar, but slightly different, using text labels, or even different opacities.  This will do that for you.

Theoretically, you could also use it to caption memes, but that hasn't been tested.


## How

You can reference the markers in two ways: using a django template tag, or directly via URL parameters.  The former is preferred, and the latter is not recommended, since it requires a hit to your application server every time, but both will work anyway.

### Using a Template Tag:

This will generate a media URL pointing to a newly-created marker based on a `template.png`, with the text `42`, positioned `3` pixels right, and `3` pixels down from the upper left corner of the template, with an opacity of 50%, and using the hex colour `#333333.  All of the arguments, save for `template` are optional:

    {% marker template='path/to/template.png' text='42' x=3 y=3 opacity=0.5 colour='333333' %}

Typically, you'll use this in your template to assign marker paths to some javascript variables:

    <script>
      var marker1 = "{% marker template='path/to/template.png' text='1' %}";
      var marker2 = "{% marker template='path/to/template.png' text='3' opacity=0.5 %}";
    </script>

After you have the URLs in your Javascript, you can do whatever you like with them, they're just URLs to static files.


### Using Direct Links

The same arguments passed to the template tag can be passed in a URL:

    https://localhost:8000/markers/marker/path/to/template.png?text=42&opacity=0.5&x=3&y=3&colour=333333


## Installation

In your `settings.py`:

    INSTALLED_APPS = (
        ...
        "markers",
    )

And if you want to make use of the direct URL requests, you'll need to add this to your core `urls.py`:

    url(r"^some/arbitrary/path/", include("markers.urls")),


### The Templates

The template path you pass to `django-markers`, either as a URL argument or in a template tag must be part of one of your apps, and referenced as such.  So for example, if you have a template living in `cartography/static/cartography/img/markers/mytemplate.png`, the argument you're looking for is: `cartography/img/markers/mytemplate.png`.


## Licensing

The whole project is licesned under the GPL-3, but the default font used is licensed under Apache 2.0.  Both licenses are available under `COPYING/`.


