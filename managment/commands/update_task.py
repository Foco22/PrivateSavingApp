from bank import tasks as bank_tasks
from django.core.management.base import BaseCommand
from bank.tasks import update_transactions_table  # Import your task here

class Command(BaseCommand):
    help = 'Run the startup task'

    def handle(self, *args, **kwargs):
        update_transactions_table()
        self.stdout.write(self.style.SUCCESS('Successfully started the task'))

