from flask_assets import Environment, Bundle

js_lodjers = Bundle("js/lodjers.js",
                    filters="jsmin", output="js/lodjers.min.js")

css_lodjers = Bundle("scss/lodjers.scss",
                     filters="pyscss", output="css/lodjers.css")

js_mixpanel = Bundle("js/vendor/mixpanel.js",
                     filters="jsmin", output="js/mixpanel.min.js")


def init_app(app):
    webassets = Environment(app)
    webassets.url = app.static_url_path
    webassets.register('js_lodjers', js_lodjers)
    webassets.register('js_mixpanel', js_mixpanel)
    webassets.register('css_lodjers', css_lodjers)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
