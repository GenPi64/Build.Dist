import os
import importlib

config = getattr(importlib.import_module('.'+os.environ['PROJECT']+'Config', 'pyconfig'), os.environ['PROJECT'])
