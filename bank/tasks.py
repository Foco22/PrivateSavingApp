import datetime
import traceback
from core.settings import EMAIL_HOST_USER
from bank import services as bank_services
from celery.utils.log import get_task_logger
from celery import shared_task
import time

logger = get_task_logger(__name__)

@shared_task
def update_transactions_table(link_token, security_token):
    logger.info("Starting update transactions table")
    transaction_data = bank_services.ExtractFintoc(link_token, security_token)
    transaction_data = transaction_data.get_movements()
    bank_services.update_transactions_table(transaction_data)

    logger.info("Finished create_and_update Bank task")
