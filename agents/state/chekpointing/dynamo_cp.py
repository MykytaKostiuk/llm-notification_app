from langgraph_dynamodb_checkpoint import DynamoDBSaver
from langgraph_dynamodb_checkpoint import configure_logging
import logging


dynamo_saver = DynamoDBSaver(
    table_name="lg-checkpoint-table"
)

configure_logging(
    level=logging.DEBUG,
    log_format="%(levelname)s: %(message)s"
)

