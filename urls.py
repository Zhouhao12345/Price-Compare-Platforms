from werkzeug.routing import Map, Rule

from views import Test

urls_patterns = Map([
    Rule('/test', endpoint=Test),
])
