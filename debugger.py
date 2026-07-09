# unified_debugger.py
# ===============================
# DEBUGGER UNIFIÉ (mode soft, stdlib ignorés)
# ===============================

import sys
import os
import ast
import re
import traceback
import warnings
import types
import importlib.abc
import importlib.util


# ===============================
# CONFIGURATION
# ===============================
DEBUG_MODE = True
LOG_FILE = "debug.log"

CRITICAL_MODULES = set()          # Modules critiques externes
OPTIONAL_MODULES = set()

# Nettoyage forcé des modules optionnels
for mod in list(OPTIONAL_MODULES):
    sys.modules.pop(mod, None)

# ===============================
# LOGGING
# ===============================
def log_debug(msg):
    if DEBUG_MODE:
        print(msg)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass

# ===============================
# AST IMPORT ANALYSIS
# ===============================
def extract_imports_from_file(path):
    imports = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=path)
    except Exception:
        return imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imports.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    return imports

def modules_in_text(text, modules):
    found = set(re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", text))
    return {m: m in found for m in modules}

# ===============================
# SOFT CRITICAL DUMMY (stdlib ignorés)
# ===============================
class SoftCriticalDummy(types.ModuleType):
    def __init__(self, name):
        super().__init__(name)
        self.__path__ = []
        self._root = name.split(".")[0]
        self._ignore = self._root in sys.builtin_module_names or self._root in getattr(sys, "stdlib_module_names", set())
        if not self._ignore:
            log_debug(f"[SOFT WARNING] Module critique manquant : {name}")

    def __getattr__(self, name):
        if self._ignore or name.startswith("_"):
            return self._soft_stub
        full_name = f"{self.__name__}.{name}"
        log_debug(f"[SOFT CRITICAL ACCESS] {full_name}")
        if full_name not in sys.modules:
            sys.modules[full_name] = SoftCriticalDummy(full_name)
        return sys.modules[full_name]

    def _soft_stub(self, *args, **kwargs):
        if not self._ignore:
            log_debug(f"[SOFT CRITICAL CALL] {self.__name__}")
        return self

    def __call__(self, *args, **kwargs):
        return self._soft_stub()

# ===============================
# DUMMY POUR MODULES OPTIONNELS
# ===============================
class DummyModule(types.ModuleType):
    def __init__(self, name):
        super().__init__(name)
        self.__path__ = []

    def __getattr__(self, name):
        full = f"{self.__name__}.{name}"
        log_debug(f"[DUMMY ACCESS] {full}")
        if full not in sys.modules:
            sys.modules[full] = DummyModule(full)
        return sys.modules[full]

    def __call__(self, *args, **kwargs):
        log_debug(f"[DUMMY CALL] {self.__name__}")
        return self

class DummyLoader(importlib.abc.Loader):
    def create_module(self, spec):
        mod = DummyModule(spec.name)
        sys.modules[spec.name] = mod
        return mod
    def exec_module(self, module): pass

class SoftCriticalLoader(importlib.abc.Loader):
    def create_module(self, spec):
        mod = SoftCriticalDummy(spec.name)
        sys.modules[spec.name] = mod
        return mod
    def exec_module(self, module): pass

# ===============================
# META PATH FINDER
# ===============================
class MissingModuleFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        root = fullname.split(".")[0]
        # ignorer stdlib
        if root in sys.builtin_module_names or root in getattr(sys, "stdlib_module_names", set()):
            return None
        if root in CRITICAL_MODULES:
            log_debug(f"[SOFT CRITICAL IMPORT] {fullname}")
            return importlib.util.spec_from_loader(fullname, SoftCriticalLoader(), is_package=True)
        if root in OPTIONAL_MODULES:
            log_debug(f"[DUMMY MODULE CREATED] {fullname}")
            return importlib.util.spec_from_loader(fullname, DummyLoader(), is_package=True)
        return None

sys.meta_path.insert(0, MissingModuleFinder())

# ===============================
# PATCHS POUR MODULES OPTIONNELS
# ===============================

# ===============================
# SOFT DEBUGGER
# ===============================
class SoftDebugger:
    def __init__(self):
        self.enabled = False
        self.errors = []

    def enable(self):
        if self.enabled: return
        self.enabled = True
        sys.excepthook = self.handle_error
        warnings.showwarning = self.handle_warning
        log_debug("[DEBUG MODE] activé")

        self.dependency_check()


        

    def dependency_check(self):
        files = ["main.py","Secure_save.py","debugger.py"]
        all_imports = set()
        for f in files:
            if os.path.exists(f):
                all_imports |= extract_imports_from_file(f)
        if not os.path.exists("main_output.txt"): return
        text = open("main_output.txt","r",encoding="utf-8").read()
        result = modules_in_text(text, all_imports)
        for m, ok in result.items():
            log_debug(f"[{'OK' if ok else 'MISSING'}] {m}")

    def handle_error(self, et, ev, tb):
        stack = "".join(traceback.format_exception(et, ev, tb))
        log_debug("\n[DEBUG ERROR]")
        log_debug(stack)
        log_debug("[STOP]\n")

    def handle_warning(self, message, category, filename, lineno, file=None, line=None):
        log_debug(f"[WARNING] {category.__name__}: {message} ({filename}:{lineno})")

    def wrap(self, func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if not isinstance(e, ImportError):
                    self.errors.append((type(e), e, e.__traceback__))
                    while self.errors:
                        etype, evalue, etrace = self.errors.pop(0)
                        print("\n[DEBUG ERROR]")
                        print(f"Type : {etype.__name__}")
                        print(f"Message : {evalue}")
                        print("".join(traceback.format_exception(etype, evalue, etrace)))
                        print("[CONTINUATION]\n")
        return wrapped

# ===============================
# INSTANCE DEBUGGER
# ===============================
_debugger_instance = SoftDebugger()

def debug():
    _debugger_instance.enable()
    return _debugger_instance

