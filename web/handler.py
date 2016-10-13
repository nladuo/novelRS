import sys
sys.path.append("../")
from lib.utils import *
from lib.model import *
from lib.config import *


def get_novels(name):
    client = init_client()

    client.close()
