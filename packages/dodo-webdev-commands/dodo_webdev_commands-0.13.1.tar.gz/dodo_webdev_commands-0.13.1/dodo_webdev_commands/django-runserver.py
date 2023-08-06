# noqa
import argparse
from dodo_commands.extra.standard_commands import DodoCommand
from dodo_commands.framework.util import remove_trailing_dashes


class Command(DodoCommand):  # noqa
    default_port = 8000

    def add_arguments_imp(self, parser):  # noqa
        parser.add_argument(
            'runserver_args',
            nargs=argparse.REMAINDER
        )

    def handle_imp(self, runserver_args, *args, **kwargs):  # noqa
        port = self.get_config("/DJANGO/port", "8000")
        self.runcmd(
            [
                self.get_config("/DJANGO/python"),
                "manage.py",
                "runserver", "0.0.0.0:%s" % port,
            ]
            + remove_trailing_dashes(runserver_args)
            + self.get_config("/DJANGO/runserver_args", []),
            cwd=self.get_config("/DJANGO/src_dir")
        )
