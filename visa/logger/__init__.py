
import logging 
import os 
from from_root import from_root
from datetime import datetime

LOG_FILE  = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir = "log"

log_dir_path = os.path.join(from_root(),log_dir)

os.makedirs(log_dir_path,exist_ok=True)

log_file_path = os.path.join(log_dir,LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    format="[ %(asctime)s ] %(name)s - %(filename)s - %(levelname)s - %(message)s"
)

logger =logging.getLogger(__name__)


