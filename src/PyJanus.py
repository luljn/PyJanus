# Main class : entry point of the platform.

from os import system 
from sys import platform

from kernel.Kernel import Kernel

"""
    _summary_ : The main class, its role is to start the Kernel.
    
"""
class Main : 
    
    @staticmethod
    def run() -> None :
        
        # Screen clearing based on OS type.
        match platform : 
            case "win32" :    
                system("cls")
            case _ :    
                system("clear")
        
        kernel:Kernel = Kernel.getInstance()
        print("\nPyJanus is working :) !")
        kernel.start()
        kernel.stop()



if __name__ == '__main__' :
    
    Main.run()