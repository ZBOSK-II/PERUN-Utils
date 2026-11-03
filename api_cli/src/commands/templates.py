from commands.base import BaseCommand


class TemplatesCommand(BaseCommand):
    def execute(self, args):
        available_templates = self.api.get_available_templates()

        if not available_templates:
            self.console.info("No available templates found")
        else:
            self.console.info(f"Found {len(available_templates)} template(s):")
            self.console.pretty_print_list(available_templates)
