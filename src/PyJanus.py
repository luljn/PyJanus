# Main class : entry point of the platform.

from argparse import ArgumentParser
from os import system, path
from sys import platform, exit

from kernel.Kernel import Kernel

"""
    _summary_ : The main class, its role is to start the Kernel.
    
"""
class Main : 
    
    #
    __parser = ArgumentParser(description="Process the execution of agents.")
    
    @staticmethod
    def run() -> None :
        
        # 
        Main.__parser.add_argument('modules', metavar='agent_type', type=str, nargs='+',
                    help='Type of the agent to execute (module name)')
        args = Main.__parser.parse_args()
        
        # Screen clearing based on OS type.
        match platform : 
            case "win32" :    
                system("cls")
            case _ :    
                system("clear")
        
        # 
        for module in args.modules :
            
            #
            if not(path.exists(module)) or not(module.endswith('.py')) : 
                print(f"[ERROR] Agent type '{module}' not found :( !")
                exit(1)
        
        #
        print("[INFO] PyJanus is working :) !\n")
        
        kernel:Kernel = Kernel.getInstance()
        kernel.start()
        print(f"Agents to spawn : {args.modules}")
        
        kernel.stop()



if __name__ == '__main__' :
    
    Main.run()