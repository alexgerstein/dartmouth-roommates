from flask_assets import Environment, Bundle

js_lodjers = Bundle("js/lodjers.js",
                      filters="jsmin", output="js/lodjers.min.js")

js_vendor = Bundle("js/vendor/angular-material.js",
                        filters="jsmin", output="js/vendor.min.js")

css_lodjers = Bundle("scss/lodjers.scss",
                        filters="pyscss", output="css/lodjers.css")

css_vendor = Bundle("css/vendor/angular-material.css",
                        filters="cssmin", output="css/vendor.min.css")


def init_app(app):
    webassets = Environment(app)
    webassets.url = app.static_url_path
    webassets.register('js_lodjers', js_lodjers)
    webassets.register('js_vendor', js_vendor)
    webassets.register('css_lodjers', css_lodjers)
    webassets.register('css_vendor', css_vendor)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
