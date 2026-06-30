"""Responder route modules (the port of kjvstudy_org/routes/*).

Each module defines a ``register(api)`` function that adds its routes to the
passed Responder API. ``register_all`` wires every module that has been ported.
"""
import importlib
import importlib.util

# Registration order mirrors server.py's include_router order. The API module is
# registered before the catch-alls; resources last (it's large).
_MODULES = [
    "main",
    "utility",
    "about",
    "topics",
    "reading_plans",
    "study",
    "timeline",
    "stories",
    "strongs",
    "study_guides",
    "family_tree",
    "commentary",
    "bible",
    "misc",
    "api",
    "resources",
]


def register_all(api):
    """Import and register every ported route module. Returns the list registered."""
    registered = []
    for name in _MODULES:
        if importlib.util.find_spec(f"{__package__}.{name}") is None:
            continue  # not ported yet (incremental build)
        importlib.import_module(f".{name}", __package__).register(api)
        registered.append(name)
    return registered
