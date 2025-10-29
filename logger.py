
import logging, os
LOG = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=LOG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('llm_redteam_backend')
