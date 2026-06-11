# PyJanus.py – Entry point of the platform

from argparse import ArgumentParser
from asyncio import run
from importlib import import_module
from os import system, path
from sys import platform, exit

from kernel.Kernel import Kernel
from kernel.ArgType import ArgType


class Main:
    
    __parser = ArgumentParser(description="Process the execution of agents.")
    __argType: ArgType = None
    
    @staticmethod
    def run() -> None:
        group = Main.__parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-f', '--file', nargs='+', metavar='FILE',
                           help="Path to one or more .py files (e.g., agent/HelloAgent.py)")
        group.add_argument('-m', '--module', nargs='+', metavar='MODULE',
                           help="Name of one or more modules (e.g., agent.HelloAgent)")
        args = Main.__parser.parse_args()
        
        if platform == "win32":
            system("cls")
        else:
            system("clear")
        
        print("[INFO] PyJanus is working :) !\n")
        
        kernel = Kernel.getInstance()
        
        # 1. Start services (non‑blocking)
        kernel.start()
        
        # 2. Spawn the requested agents
        if args.file:
            Main.__argType = ArgType.FILE
            for file in args.file:
                if not path.exists(file) or not file.endswith('.py'):
                    print(f"[ERROR] Agent type '{file}' not found.")
                    exit(1)
            print(f"\n[INFO] Agents to spawn : {args.file}\n")
            for file in args.file:
                run(kernel.spawn(ArgType.FILE, file))
        
        elif args.module:
            Main.__argType = ArgType.MODULE
            for module in args.module:
                try:
                    import_module(module)
                except ModuleNotFoundError:
                    print(f"[ERROR] Agent module '{module}' not found.")
                    exit(1)
                except Exception as e:
                    print(f"[ERROR] Something went wrong while importing '{module}': {e}")
                    exit(1)
            print(f"\n[INFO] Agents to spawn : {args.module}\n")
            for module in args.module:
                run(kernel.spawn(ArgType.MODULE, module))
        
        # 3. Wait for all agents to finish (blocking)
        kernel.wait_for_completion()


if __name__ == '__main__':
    Main.run()