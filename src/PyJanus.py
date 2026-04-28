# Main class : entry point of the platform.

from os import system 
from sys import platform, argv, exit

from kernel.Kernel import Kernel

"""
    _summary_ : The main class, its role is to start the Kernel.
    
"""
class Main : 
    
    __agents = {} # Agents to spawn (name & type).
    
    @staticmethod
    def run() -> None :
        
        # Screen clearing based on OS type.
        match platform : 
            case "win32" :    
                system("cls")
            case _ :    
                system("clear")
        
        # if the user does not provide the required arguments (agent type & name)
        if ((len(argv)-1)%2 !=0 ) :
            
            print("Usage : python PyJanus.py Type_Agent Name_Agent ...")
            print("You must provide at least one agent type and a name for the agent")
            print("When you provide an agent type, you must provide a name for the agent\n")
            exit(1)
        
        else :
            
            print("\nPyJanus is working :) !\n")
            
            kernel:Kernel = Kernel.getInstance()
            kernel.start()
            
            for i in range(1, len(argv), 2) :
                
                print(f"Spawn {argv[i+1]} of type {argv[i]}...")
                Main.__agents[argv[i+1]] = argv[i]
            
            print(Main.__agents)
            kernel.stop()



if __name__ == '__main__' :
    
    Main.run()