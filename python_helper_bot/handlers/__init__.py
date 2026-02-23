from .start import router as start_router
from .content import router as content_router
from .search import router as search_router
from .errors import router as errors_router
from .favorites import router as favorites_router

__all__ = [
    "start_router", 
    "content_router",
    "search_router", 
    "errors_router",
    "favorites_router"
]
