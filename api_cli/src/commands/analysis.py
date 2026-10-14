from commands.base import BaseCommand


class AnalysisCommand(BaseCommand):
    def execute(self, args):
        analysis = self.api.get_analysis(args.task_uid)

        if not analysis:
            self.console.info("No analysis found")
        else:
            self.console.json(analysis)
