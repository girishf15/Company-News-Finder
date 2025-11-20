import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
FIXTURES_DIR = os.path.join(BASE_DIR, "../fixtures")

STATUS_PROCESSING = "Processing"
STATUS_COMPLETED = "Completed"
STATUS_FAILED = "Failed"

THRESHOLD_SCORE = 20