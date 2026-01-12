"""
Pluggy-based hooks system with granular per-item priorities.

Each item (model, schema, service, router) has its own priority.
Higher priority wins for items with the same name/prefix.

Example:
    # In update v1
    return {"BookModel": (1, BookModel)}

    # In patch - override BookModel with higher priority
    return {"BookModel": (2, NewBookModel)}
"""

import logging
import pluggy

from typing import Any, Dict, Type


logger = logging.getLogger(__name__)

hookspec = pluggy.HookspecMarker("fastapi_app")
hookimpl = pluggy.HookimplMarker("fastapi_app")


class AppHookSpec:
    """Hook specifications for the plugin system."""

    @hookspec
    def register_models(self) -> Dict[str, tuple[int, Type]]:
        """
        Register SQLAlchemy models.

        Returns:
            Dict mapping model name to (priority, model_class)
            Example: {"BookModel": (1, BookModel), "UserModel": (1, UserModel)}
        """

    @hookspec
    def register_schemas(self) -> Dict[str, tuple[int, Type]]:
        """
        Register Pydantic schemas.

        Returns:
            Dict mapping schema name to (priority, schema_class)
            Example: {"BookSchema": (1, BookSchema)}
        """

    @hookspec
    def register_services(self, session_factory) -> Dict[str, tuple[int, Any]]:
        """
        Register service functions.

        Args:
            session_factory: Async session factory for database operations

        Returns:
            Dict mapping function name to (priority, function)
            Example: {"get_all_books": (1, get_all_books)}
        """

    @hookspec
    def register_routers(self) -> Dict[str, tuple[int, Any]]:
        """
        Register FastAPI routers.

        Returns:
            Dict mapping route prefix to (priority, router)
            Example: {"/books": (1, books_router), "/users": (1, users_router)}
        """


class HooksRegistry:
    """
    Global registry for all hooks results.
    Stores merged results with priority resolution.
    """

    def __init__(self):
        self._models: Dict[str, Type] = {}
        self._schemas: Dict[str, Type] = {}
        self._services: Dict[str, Any] = {}
        self._routers: Dict[str, Any] = {}

    @property
    def models(self) -> Dict[str, Type]:
        """Get all registered models."""

        return self._models

    @property
    def schemas(self) -> Dict[str, Type]:
        """Get all registered schemas."""

        return self._schemas

    @property
    def services(self) -> Dict[str, Any]:
        """Get all registered service functions."""

        return self._services

    @property
    def routers(self) -> Dict[str, Any]:
        """Get all registered routers."""

        return self._routers

    def get_model(self, name: str) -> Type | None:
        """Get model by name."""

        return self._models.get(name)

    def get_schema(self, name: str) -> Type | None:
        """Get schema by name."""

        return self._schemas.get(name)

    def get_service(self, name: str) -> Any | None:
        """Get service function by name."""

        return self._services.get(name)

    def get_router(self, prefix: str) -> Any | None:
        """Get router by prefix."""

        return self._routers.get(prefix)


registry: HooksRegistry = HooksRegistry()


def merge_with_priority(
    existing: Dict[str, Any],
    new_items: Dict[str, tuple[int, Any]],
    priorities: Dict[str, int],
    category: str
) -> None:
    """
    Merge new items into existing dict using priority resolution.

    Args:
        existing: Dict to merge into (modified in place)
        new_items: Dict of name -> (priority, item)
        priorities: Dict tracking current priority for each name
        category: Category name for logging
    """
    for name, (priority, item) in new_items.items():
        current_priority = priorities.get(name, -1)
        if priority > current_priority:
            if name in existing:
                logger.debug(f"{category} '{name}': priority {priority} > {current_priority}, overriding")
            existing[name] = item
            priorities[name] = priority
        else:
            logger.debug(f"{category} '{name}': priority {priority} <= {current_priority}, skipping")
