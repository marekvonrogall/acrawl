from enum import Enum
from datetime import datetime

FETCHING_DATE = datetime.today().strftime("%Y-%m-%d")
BASE_DIR = "data"

class Color:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class Frequency(Enum):
    AIA_193 = "0193"
    AIA_304 = "0304"
    AIA_171 = "0171"
    AIA_211 = "0211"
    AIA_131 = "0131"
    AIA_335 = "0335"
    AIA_094 = "0094"
    AIA_1600 = "1600"
    AIA_1700 = "1700"

DEFAULT_FREQUENCY = Frequency.AIA_171

class Resolution(Enum):
    R512 = "512"
    R1024 = "1024"
    R2048 = "2048"
    R4096 = "4096"

DEFAULT_RESOLUTION = Resolution.R1024

class Corner(Enum):
    FULL = ""
    CLOSEUP = "NC_"
    NW = "NW_"
    NE = "NE_"
    SW = "SW_"
    SE = "SE_"

DEFAULT_CORNER = Corner.FULL
