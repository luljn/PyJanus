# Main class : entry point of the platform.

from argparse import ArgumentParser
from asyncio import run
from importlib import import_module
from os import system, path
from sys import platform, exit

from kernel.Kernel import Kernel
from kernel.ArgType import ArgType
from services.DirectoryService import DirectoryService

"""
    _summary_ : The main class, its role is to start the Kernel.
    
"""
class Main : 
    
    # Class attributes.
    __parser = ArgumentParser(description="Process the execution of agents.")
    __argType: ArgType = None
    
    @staticmethod
    def run() -> None :
        
        # Command Line args definition
        group = Main.__parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-f', '--file', nargs='+', metavar='FICHIER',
                    help="Path to one or more .py files (e.g : agent/HelloAgent.py)")
        group.add_argument('-m', '--module', nargs='+', metavar='MODULE',
                    help="Name of one or more modules (e.g., agent.HelloAgent)")
        args = Main.__parser.parse_args()
        
        # Screen clearing based on OS type.
        match platform : 
            case "win32" :    
                system("cls")
            case _ :    
                system("clear")
        
        # System info on VM status.
        print("[INFO] PyJanus is working :) !\n")
        
        kernel:Kernel = Kernel.getInstance()
        kernel.start()
        
        # If files used
        if args.file :
            
            Main.__argType = ArgType.FILE
            # Testing on args.
            for file in args.file :
                
                if not(path.exists(file)) or not(file.endswith('.py')) : 
                    print(f"[ERROR] Agent type '{file}' not found :( ! Please check the file name")
                    exit(1)
            
            """ print(f"\r[INFO] Agents to spawn : {args.file}", end=" ", flush=True) """
            print(f"\n\r[INFO] Agents to spawn : {args.file}\n")
            for file in args.file :
                run(kernel.spawn(ArgType.FILE, file))
        
        # If modules used
        elif args.module :
            
            Main.__argType = ArgType.MODULE
            # Testing on args.
            for module in args.module :
                
                try :
                    import_module(module)
                    #print(f"\n\r[INFO] Agents to spawn : {args.module}", end=" ", flush=True)
                
                except ModuleNotFoundError :
                    print(f"[ERROR] : Agent '{module}' not found :( ! Please check the module name.")
                    exit(1)
                
                except Exception as e :
                    print(f"[ERROR] : Something went wrong while executing '{module}' : {e}")
                    exit(1)
            
            print(f"\n\r[INFO] Agents to spawn : {args.module}\n")
            for module in args.module :
                run(kernel.spawn(ArgType.MODULE, module))
        
        print(kernel.getDefaultSpace().getParticipants())
        print(kernel.getService(DirectoryService).getNumberOfAgents())
        kernel.stop() # To remove, it is just for testing.



if __name__ == '__main__' :
    
    Main.run()