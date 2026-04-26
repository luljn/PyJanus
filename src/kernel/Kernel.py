###


class Kernel : 
    
    instance = None
    
    #
    def __init__(self):
        
        self.services = []
        self.defaultSpace = None
        self.running: bool = False
        self.mainThread = None
    
    #
    @staticmethod
    def getInstance() : 
        
        if (Kernel.instance is None) :
            Kernel.instance = Kernel()
            
        return Kernel.instance
    
    #
    def start(self) -> None : 
        
        self.running = True
        print("Kernel started successfully :) !\n")
    
    #
    def stop(self) -> None :
        
        print("Kernel stoped without error :) !\n")
        self.running = False
    
    #
    def getService(self) :
        pass
    
    #
    def spawn(self) :
        pass
    
    #
    def getDefaultSpace(self) :
        
        return self.defaultSpace