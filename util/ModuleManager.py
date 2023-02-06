import asyncio
import os
from importlib import import_module
from inspect import getmembers, isfunction


class ModuleManager:
    def __init__(self):
        self.modules = {}
        self.base_path = os.path.dirname(os.getcwd() + "/modules")

    def load_modules(self, logger, modules):
        prefix = "module_manager"
        logger.log_message(prefix, "Loading modules...")
        logger.log_message(prefix, f"module list: {str(list(modules.keys()))}")
        for module in modules:
            # logger.log_message(prefix, f"Processing module: {module}")
            # logger.log_message(prefix, f"module_data: {modules[module]}")
            if modules[module]["enabled"]:
                logger.log_message(prefix, f"module enabled: {module}")
                # logger.log_message(prefix, f"module directory: {modules[module]['dir']}")

                # import the module into the global table
                self.modules[module] = import_module(f"modules.{modules[module]['dir']}.{module}")
                # logger.log_message(prefix, f"module imported: {self.modules[module]}")

                # process functions imported from the module
                functions_list = []
                functions_list_touples = getmembers(self.modules[module], isfunction)
                for toup in functions_list_touples:
                    functions_list.append(toup[0])
                logger.log_message(prefix, f"worker functions in [{module}]: " + str(functions_list))

                # Load service workers
                for function in functions_list_touples:
                    if function[0].endswith("Worker"):
                        if function[0].startswith("_") or function[0].startswith("<function"):
                            continue
                        # logger.log_message(prefix, f"Loading service worker: {function[0]}")
                        # logger.log_message(prefix, "module touple function[1]: " + str(type(function[1])))
                        logger.log_message(prefix, f"Starting coroutine: {function[0]}")
                        import_func_coroutine = function[1]
                        asyncio.ensure_future(import_func_coroutine(logger))

    def get_modules(self):
        return self.modules
