__import__('os').environ['TZ'] = 'UTC'
import time
if hasattr(time, 'tzset'):
    time.tzset()

import logging
from app import utils, ui, web_api

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(utils.log_path),
        logging.StreamHandler()
    ]
)
_logger = logging.getLogger(__name__)
main_ui = ui.ViinSignUI()

if __name__ == '__main__':
    _logger.info('---------Start Application----------')
    web_api.server_service.start_api_service()
    main_ui.start_ui(on_close=web_api.server_service.stop_api_service)
