# MAIN CLASS

from kernel.Kernel import Kernel

from os import system 
from sys import platform

"""The main class : its role is to start the Kernel.
"""
class Main : 
    
    @staticmethod
    def run() -> None :
        
        # OS recognition for clearing screen.
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