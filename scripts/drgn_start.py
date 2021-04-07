import drgn
from drgn import NULL, Object, cast, container_of, execscript, offsetof, reinterpret, sizeof
from drgn.helpers.linux import *
import os
prog = drgn.program_from_kernel()

