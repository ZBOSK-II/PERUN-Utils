from commands.base import BaseCommand


class FilesCommand(BaseCommand):
    def execute(self, args):
        files = self.api.get_files(args.task_uid)

        self.console.info(f"Files for task {args.task_uid}:")
        self.console.pretty_print_list(files)
