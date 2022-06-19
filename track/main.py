from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal

from .controllers.tasks import Tasks
from .core.exc import TrackError
from .controllers.base import Base
from .controllers.projects import Projects
from .controllers.task_types import TaskTypes
from sqlalchemy import create_engine
from os import path
from alembic.config import Config
from alembic import command


# configuration defaults
CONFIG = init_defaults("track")
CONFIG["track"]["db"] = "~/.track/track5.db"

def migrate_db(migrations_path, db_path, alembic_ini_path=None, revision="head"):
    config = Config(alembic_ini_path)
    config.set_main_option('script_location', migrations_path)
    config.set_main_option('sqlalchemy.url', f"sqlite:///{db_path}")
    command.upgrade(config, revision)

def db_setup(app):
    app.log.debug("DB engine setup")
    db_path = path.expanduser(app.config.get("track", "db"))
    db_status = path.exists(db_path)
    engine = create_engine(f"sqlite:///{db_path}", future=True)
    if not db_status:
        app.log.info(f"Create DB structure for {db_path}.")
        migrate_db(migrations_path='alembic/', db_path=db_path, alembic_ini_path='./alembic.ini')
    app.extend("db_engine", engine)


class Track(App):
    """Time Tracker primary application."""

    class Meta:
        hooks = [("pre_run", db_setup)]

        label = "track"

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            "yaml",
            "colorlog",
            "jinja2",
        ]

        # configuration handler
        config_handler = "yaml"

        # configuration file suffix
        config_file_suffix = ".yml"

        # set the log handler
        log_handler = "colorlog"

        # set the output handler
        output_handler = "jinja2"

        # register handlers
        handlers = [Base, Projects, TaskTypes, Tasks]


class TrackTest(TestApp, Track):
    """A sub-class of Track that is better suited for testing."""

    class Meta:
        label = "track"


def main():
    with Track() as app:
        try:
            app.run()

        except AssertionError as e:
            print("AssertionError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except TrackError as e:
            print("TrackError > %s" % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback

                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print("\n%s" % e)
            app.exit_code = 0


if __name__ == "__main__":
    main()
