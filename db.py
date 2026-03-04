import mysql.connector
# force inclusion of certain submodules when bundling with PyInstaller
# the pure implementation will try to load locale and plugin modules at
# runtime; if they are missing an ImportError occurs in the frozen app.
try:
    import mysql.connector.locales.eng.client_error  # type: ignore
    import mysql.connector.plugins.mysql_native_password  # type: ignore
except ImportError:
    # ignore if running in a minimal environment where these are not available
    pass

import configparser
import os
import sys
from pathlib import Path


def conectar():
    # determine the location of config.ini
    # when running as a script it's next to the repository root,
    # when bundled by PyInstaller the file should be placed next to
    # the executable (or added as a data file and extracted to _MEIPASS).
    config = configparser.ConfigParser()

    # default search order:
    # 1. directory of the frozen executable (PyInstaller)
    # 2. parent of this module (the project root when running from source)
    # 3. current working directory (fallback)
    if getattr(sys, "frozen", False):
        # PyInstaller puts files into _MEIPASS or the executable's folder
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent.parent

    config_path = base / "config.ini"
    if not config_path.exists():
        config_path = Path.cwd() / "config.ini"

    config.read(config_path)

    try:
        # use the pure Python implementation to avoid issues with
        # the C extension when the app is bundled as an executable.
        return mysql.connector.connect(
            host=config["database"]["host"],
            user=config["database"]["user"],
            password=config["database"]["password"],
            database=config["database"]["database"],
            use_pure=True
        )
    except Exception as err:
        # log the error to a file in the executable directory
        msg = f"Database connection failed: {err!r}\n"
        try:
            with open(base / "db_error.log", "a", encoding="utf-8") as f:
                f.write(msg)
        except Exception:
            pass
        # re‑raise so the caller knows something went wrong
        raise

