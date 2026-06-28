from . import kjv

# NOTE: the FastAPI app (``server``) is intentionally NOT imported here. The
# Responder port (responder_app) and FastAPI (server) require incompatible
# Starlette versions, so importing the package must not force-load either web
# layer. Import ``kjvstudy_org.server`` or ``kjvstudy_org.responder_app``
# explicitly depending on which app you're running.
