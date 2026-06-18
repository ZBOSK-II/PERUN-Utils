from commands.base import BaseCommand


class ListCommand(BaseCommand):
    def execute(self, args):
        tasks = self.api.list_tasks()

        if not tasks:
            self.console.info("No tasks found")
        else:
            self.console.info(f"Found {len(tasks)} task(s):")
            self.console.pretty_print_list(tasks)
