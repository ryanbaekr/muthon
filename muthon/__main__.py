"""CLI for Muthon"""

import sys

from .cli_parser import parse_args
from .sca import run_sca

kwargs = parse_args()

if run_sca(**kwargs):
    sys.exit(0)
sys.exit(1)
