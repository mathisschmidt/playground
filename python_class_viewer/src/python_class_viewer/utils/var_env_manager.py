import inspect
import logging
import os

logger = logging.getLogger(__name__)

class VarEnvManager:

    def __init__(self):
        pass

    @property
    def database_url(self) -> str | None:
        return os.getenv("PYTHON_CLASS_VIEWER_DATABASE_URL")

    @property
    def port_server(self) -> int | None:
        port = os.getenv("PYTHON_CLASS_VIEWER_PORT_SERVER")
        if port:
            if not port.isdigit():
                logger.error("Environment variable 'PYTHON_CLASS_VIEWER_PORT_SERVER' must be an integer. Ignored.")
            else:
                port = int(port)
        return port

    def check_availability(self) -> bool:
        found_any = False
        checked = []
        properties = [name for name, value in inspect.getmembers(type(self)) if isinstance(value, property)]
        logger.debug(f"Found {len(properties)} properties on {type(self)}")

        for name in properties:
            try:
                val = getattr(self, name)
            except Exception as exc:  # property access raised
                logger.error("Error reading property '%s': %s", name, exc)
                val = None
            if val is not None:
                found_any = True
                logger.info("Environment value found for '%s': %r", name, val)
            else:
                logger.info("No environment value for '%s'", name)

            checked.append(name)
        logger.debug("Checked properties: %s", checked)
        return found_any


class SingletonVarEnvManager(VarEnvManager):
    _initialized: bool = False
    _instance: VarEnvManager | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonVarEnvManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__()
            self._initialized = True