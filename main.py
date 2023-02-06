import asyncio
import tracemalloc

from util.ConfigManager import ConfigManager
from util.LogManager import LogManager
from util.ModuleManager import ModuleManager

# enable tracing memory allocations for this program
tracemalloc.start()

config_manager = ConfigManager()
config = config_manager.get_config()

log_manager = LogManager()
log = log_manager.get_log()

module_manager = ModuleManager()

if __name__ == "__main__":
    log_manager.log_message("daemon", "Starting daemon...")
    loop = asyncio.get_event_loop()
    try:
        # load modules
        modules = config["modules"]
        module_manager.load_modules(log_manager, modules)

        # start program loop
        loop.run_forever()
    except KeyboardInterrupt:
        log_manager.log_message("daemon", "process interrupted by [CTRL + ^C]")
        pass
    finally:
        log_manager.log_message("daemon", "Closing Loops")
        tasks = asyncio.all_tasks(loop)
        log_manager.log_message("daemon", f"Cancelling {len(tasks)} outstanding asyncio tasks")
        for task in tasks:
            task.done()
        loop.close()
