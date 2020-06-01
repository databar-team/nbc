import os
from typing import Union

from kasasa_common.context import Context, DatabaseContext, get_database_reader_config, get_database_writer_config, \
    get_env_vars, ProducerConsumerContext
from kasasa_common.logger import logger

from config import WORKER_SQL_PATH


class ServiceContext(Context):
    def __init__(self, **kwargs):
        self.WORK_QUEUE_CONTEXT: WorkQueueContext = kwargs.get('WORK_QUEUE_CONTEXT', None)


class MarketingCloudClientContext(Context):
    def __init__(self, **kwargs):
        self.AUTH_URL = kwargs.get('AUTH_URL', None)
        self.AUTH_ID = kwargs.get('AUTH_ID', None)
        self.AUTH_SECRET_KEY = kwargs.get('AUTH_SECRET_KEY', None)
        self.GET_PRODUCT_DATA_URL = kwargs.get('GET_PRODUCT_DATA_URL', None)
        self.SECRETS = kwargs.get('SECRETS', {self.AUTH_SECRET_KEY: ""})


class WorkerContext(Context):
    def __init__(self, **kwargs):
        self.WRITER_CONTEXT: DatabaseContext = kwargs.get('DATABASE_CONTEXTS', dict()).get('reader', None)
        self.READER_CONTEXT: DatabaseContext = kwargs.get('DATABASE_CONTEXTS', dict()).get('writer', None)
        self.PRODUCER_CONSUMER_CONTEXT: ProducerConsumerContext = kwargs.get(
            'PRODUCER_CONSUMER_CONTEXT', ProducerConsumerContext())
        self.WORK_QUEUE_CONTEXT: WorkQueueContext = kwargs.get('WORK_QUEUE_CONTEXT', None)
        self.MARKETING_CLOUD_CONTEXT: MarketingCloudClientContext = kwargs.get('MARKETING_CLOUD_CONTEXT', None)
        self.SQL_PATH = kwargs.get('SQL_PATH', None)
        self.SLEEP_TIME = kwargs.get('WORKER_SLEEP_TIME', 60)


class WorkQueueContext(Context):
    def __init__(self, **kwargs):
        self.TYPE = kwargs.get('TYPE', 'filesystem')
        self.PATH = kwargs.get('PATH', './work-queue')


def build_context(context_type: str, **kwargs) -> Union[ServiceContext, WorkerContext]:
    env_vars = get_env_vars(
        required_env_vars=[],
        **kwargs
    )

    # database contexts
    def get_database_contexts(secrets):
        reader_config = get_database_reader_config(**env_vars)
        writer_config = get_database_writer_config(**env_vars)
        return dict(
            writer=DatabaseContext(**writer_config, VAULT_SECRETS=secrets),
            reader=DatabaseContext(**reader_config, VAULT_SECRETS=secrets)
        )

    # marketing cloud client context
    def get_marketingcloud_client_context(secrets):
        return MarketingCloudClientContext(
            AUTH_URL=os.getenv('MC_AUTH_URL', None),
            AUTH_ID=os.getenv('MC_AUTH_ID', None),
            AUTH_SECRET_KEY=os.getenv('MC_AUTH_SECRET_KEY', None),
            GET_PRODUCT_DATA_URL=os.getenv('MC_GET_PRODUCT_DATA_URL', None),
            SECRETS=secrets
        )

    # work queue context
    def get_work_queue_context():
        return WorkQueueContext(
            TYPE=os.getenv('WORK_QUEUE_TYPE', 'filesystem'),
            PATH=os.getenv('WORK_QUEUE_PATH', './work_queue')
        )

    # service context
    def get_service_context():
        return ServiceContext(
            WORK_QUEUE_CONTEXT=get_work_queue_context(),
            **env_vars
        )

    # worker context
    def get_worker_context(secrets):
        return WorkerContext(
            DATABASE_CONTEXTS=get_database_contexts(secrets),
            WORK_QUEUE_CONTEXT=get_work_queue_context(),
            PRODUCER_CONSUMER_CONTEXT=ProducerConsumerContext(
                QUEUE_TYPE='memory',
                QUEUE_KWARGS=dict(max_size=50),
                MAX_CONSUMERS=5
            ),
            MARKETING_CLOUD_CONTEXT=get_marketingcloud_client_context(secrets),
            SQL_PATH=WORKER_SQL_PATH,
            **env_vars
        )

    # App context
    if context_type == 'service':
        return get_service_context()
    if context_type == 'worker':
        from util.secrets import get_secrets
        secrets_dict = get_secrets(logger)
        return get_worker_context(secrets_dict)
