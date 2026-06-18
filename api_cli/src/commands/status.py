from commands.base import BaseCommand


class StatusCommand(BaseCommand):
    def execute(self, args):
        status_data = self.api.get_status(args.task_uid)

        if not status_data:
            self.console.warning(f"No status found for task with id {args.task_uid}")
        else:
            self.console.info(f"Status data for {args.task_uid}:")
            self.console.json(status_data)
