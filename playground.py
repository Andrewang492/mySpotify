class MyObject:
    # data
    def __init__(self, data:str) -> None:
        self.data = data
    
    def getData(self) -> str:
        if self.data:
            return self.data
        return None
    
if __name__ == '__main__':
    newObj = MyObject("data 1")
    print(newObj.getData())