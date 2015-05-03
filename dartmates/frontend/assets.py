from flask_assets import Environment, Bundle

js_dartmates = Bundle("js/dartmates.js",
                      filters="jsmin", output="js/dartmates.min.js")

css_dartmates = Bundle("scss/dartmates.scss",
                        filters="pyscss", output="css/dartmates.css")

def init_app(app):
    webassets = Environment(app)
    webassets.url = app.static_url_path
    webassets.register('js_dartmates', js_dartmates)
    webassets.register('css_dartmates', css_dartmates)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = app.debug
