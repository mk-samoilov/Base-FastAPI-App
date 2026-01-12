"""
Updates engine for loading and registering update plugins.

Auto-discovers update modules from app/updates/ directory.
Each module should have an UpdatePlugin class implementing hooks.
"""

import importlib
import logging
import pluggy

from pathlib import Path

from .hooks import AppHookSpec, merge_with_priority, registry


logger = logging.getLogger(__name__)


def initialize_updates(session_factory) -> pluggy.PluginManager:
    """
    Initialize updates system by loading all update plugins.

    Scans app/updates/ for directories containing UpdatePlugin classes.
    Registers all plugins and merges their contributions using priority system.

    Args:
        session_factory: Async session factory for database operations

    Returns:
        PluginManager with all updates registered
    """

    pm = pluggy.PluginManager("fastapi_app")
    pm.add_hookspecs(AppHookSpec)

    updates_dir = Path(__file__).parent.parent / "updates"
    logger.info(f"Scanning for updates in: {updates_dir}")

    if not updates_dir.exists():
        logger.warning(f"Updates directory not found: {updates_dir}")
        return pm

    for path in sorted(updates_dir.iterdir()):
        if path.is_dir() and not path.name.startswith("_"):
            try:
                module = importlib.import_module(f"app.updates.{path.name}")

                if hasattr(module, "UpdatePlugin"):
                    plugin_class = getattr(module, "UpdatePlugin")
                    plugin_instance = plugin_class()
                    pm.register(plugin_instance, name=path.name)
                    logger.info(f"Registered update plugin: {path.name}")
                else:
                    logger.debug(f"No UpdatePlugin in {path.name}, skipping")

            except Exception as e:
                logger.error(f"Failed to load update {path.name}: {e}", exc_info=True)

    model_priorities: dict[str, int] = {}
    schema_priorities: dict[str, int] = {}
    service_priorities: dict[str, int] = {}
    router_priorities: dict[str, int] = {}

    for result in pm.hook.register_models():
        if result:
            merge_with_priority(
                registry._models,
                result,
                model_priorities,
                "Model"
            )
    logger.info(f"Registered {len(registry._models)} models")

    for result in pm.hook.register_schemas():
        if result:
            merge_with_priority(
                registry._schemas,
                result,
                schema_priorities,
                "Schema"
            )
    logger.info(f"Registered {len(registry._schemas)} schemas")

    for result in pm.hook.register_services(session_factory=session_factory):
        if result:
            merge_with_priority(
                registry._services,
                result,
                service_priorities,
                "Service"
            )
    logger.info(f"Registered {len(registry._services)} services")

    for result in pm.hook.register_routers():
        if result:
            merge_with_priority(
                registry._routers,
                result,
                router_priorities,
                "Router"
            )
    logger.info(f"Registered {len(registry._routers)} routers")

    return pm
