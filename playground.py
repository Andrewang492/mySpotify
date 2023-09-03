class MyObject:
    # data
    def __init__(self, data:str) -> None:
        self.data = data
        self.dicti = {'a':1, 'b':2,'c':33}
    
    def getData(self) -> str:
        if self.data:
            return self.data
        return None
    def getDict(self) ->dict:
        return self.dicti

# highest value pair less than x, of ordered list.
def binarySearch(x, list):
        print(f"searching for {x}")
        if list[0] > x:
            return -1
        n = len(list)
        lo = 0
        hi = n - 1
        mid = (hi+lo)//2
        #print(lo, mid, hi)
        while lo <= hi:
            if list[mid] <= x:
                # we could want this value. So don't remove it.
                if lo == mid: # i.e if nothing changes, this is the number.
                    break
                lo = mid
            else: # if that number is too big, it certainly shouldnt be considered.
                hi = mid - 1
            mid = (hi+lo)//2
            #print(lo, mid, hi)
        if list[hi] <= x:
            return list[hi]
        return list[lo]

def binSearchTest():
    list = [11, 13, 14, 18, 19, 25, 29] 
    assert(binarySearch(10, list) == -1)    
    assert(binarySearch(11, list) == 11)    
    assert(binarySearch(12, list) == 11)
    assert(binarySearch(13, list) == 13)
    assert(binarySearch(14,list) == 14)
    assert(binarySearch(15,list) == 14)
    assert(binarySearch(18, list) == 18)
    assert(binarySearch(19, list) == 19)
    assert(binarySearch(22, list) == 19)
    assert(binarySearch(25, list) == 25)  
    assert(binarySearch(27, list) == 25)  
    assert(binarySearch(29, list) == 29)
    assert(binarySearch(30, list) == 29)
    list = [11, 13, 14, 18, 19, 25]
    assert(binarySearch(10, list) == -1)    
    assert(binarySearch(11, list) == 11)    
    assert(binarySearch(12, list) == 11)
    assert(binarySearch(13, list) == 13)
    assert(binarySearch(14,list) == 14)
    assert(binarySearch(15,list) == 14)
    assert(binarySearch(18, list) == 18)
    assert(binarySearch(19, list) == 19)
    assert(binarySearch(22, list) == 19)
    assert(binarySearch(25, list) == 25)  
    assert(binarySearch(27, list) == 25) 

# lowest value higher than or equal x, of ordered list. Favour left in ties.
def lowestHigherThanX(x, list):
        print(f"searching for {x}")
        if list[len(list)-1] < x:
            return -1
        n = len(list)
        lo = 0
        hi = n - 1
        mid = (hi+lo)//2
        #print(lo, mid, hi)
        while lo <= hi:
            if list[mid] >= x:
                # we could want this value. So don't remove it.
                if hi == mid: # i.e if nothing changes, this is the number.
                    break
                hi = mid
            else: # if that number is too small, it and all smaller numbers are too small.
                lo = mid + 1
            mid = (hi+lo)//2
            #print(lo, mid, hi)

        # may be left with two values. Return lowest if it is valid, otherwise the other one.
        if list[lo] >= x:
            return list[lo]
        return list[hi]

def lowestHigherThanTest():
    list = [11, 13, 14, 18, 19, 25, 29] 
    assert(lowestHigherThanX(10, list) == 11)    
    assert(lowestHigherThanX(11, list) == 11)    
    assert(lowestHigherThanX(12, list) == 13)
    assert(lowestHigherThanX(13, list) == 13)
    assert(lowestHigherThanX(14,list) == 14)
    assert(lowestHigherThanX(15,list) == 18)
    assert(lowestHigherThanX(18, list) == 18)
    assert(lowestHigherThanX(19, list) == 19)
    assert(lowestHigherThanX(22, list) == 25)
    assert(lowestHigherThanX(25, list) == 25)  
    assert(lowestHigherThanX(27, list) == 29)  
    assert(lowestHigherThanX(29, list) == 29)
    assert(lowestHigherThanX(30, list) == -1)
    list = [11, 13, 14, 18, 19, 25]
    assert(lowestHigherThanX(10, list) == 11)    
    assert(lowestHigherThanX(11, list) == 11)    
    assert(lowestHigherThanX(12, list) == 13)
    assert(lowestHigherThanX(13, list) == 13)
    assert(lowestHigherThanX(14,list) == 14)
    assert(lowestHigherThanX(15,list) == 18)
    assert(lowestHigherThanX(18, list) == 18)
    assert(lowestHigherThanX(19, list) == 19)
    assert(lowestHigherThanX(22, list) == 25)
    assert(lowestHigherThanX(25, list) == 25)
    assert(lowestHigherThanX(30, list) == -1)

def lowestHigherThanXIndex(x, list):
        print(f"searching for {x}")
        if list[len(list)-1] < x:
            return -1
        n = len(list)
        lo = 0
        hi = n - 1
        mid = (hi+lo)//2
        #print(lo, mid, hi)
        while lo <= hi:
            if list[mid] >= x:
                # we could want this value. So don't remove it.
                if hi == mid: # i.e if nothing changes, this is the number.
                    break
                hi = mid
            else: # if that number is too small, it and all smaller numbers are too small.
                lo = mid + 1
            mid = (hi+lo)//2
            #print(lo, mid, hi)

        # may be left with two values. Return lowest if it is valid, otherwise the other one.
        if list[lo] >= x:
            return lo
        return hi

def lowestHigherThanIndexTest():
    list = [11, 13, 14, 18, 19, 25, 29] 
    assert(lowestHigherThanXIndex(10, list) == 0)    
    assert(lowestHigherThanXIndex(11, list) == 0)    
    assert(lowestHigherThanXIndex(12, list) == 1)
    assert(lowestHigherThanXIndex(13, list) == 1)
    assert(lowestHigherThanXIndex(14,list) == 2)
    assert(lowestHigherThanXIndex(15,list) == 3)
    assert(lowestHigherThanXIndex(18, list) == 3)
    assert(lowestHigherThanXIndex(19, list) == 4)
    assert(lowestHigherThanXIndex(22, list) == 5)
    assert(lowestHigherThanXIndex(25, list) == 5)  
    assert(lowestHigherThanXIndex(27, list) == 6)  
    assert(lowestHigherThanXIndex(29, list) == 6)
    assert(lowestHigherThanXIndex(30, list) == -1)
    list = [11, 13, 14, 18, 19, 25]
    assert(lowestHigherThanXIndex(10, list) == 0)    
    assert(lowestHigherThanXIndex(11, list) == 0)    
    assert(lowestHigherThanXIndex(12, list) == 1)
    assert(lowestHigherThanXIndex(13, list) == 1)
    assert(lowestHigherThanXIndex(14,list) == 2)
    assert(lowestHigherThanXIndex(15,list) == 3)
    assert(lowestHigherThanXIndex(18, list) == 3)
    assert(lowestHigherThanXIndex(19, list) == 4)
    assert(lowestHigherThanXIndex(22, list) == 5)
    assert(lowestHigherThanXIndex(25, list) == 5)
    assert(lowestHigherThanXIndex(25, list) == 5)
    assert(lowestHigherThanXIndex(30, list) == -1)
    list = [55, 55, 55]
    assert(lowestHigherThanXIndex(55, list) == 0)
    assert(lowestHigherThanXIndex(50, list) == 0)   
    list = [55, 55, 55, 55]
    assert(lowestHigherThanXIndex(55, list) == 0)
    assert(lowestHigherThanXIndex(50, list) == 0)
    list = [15, 18, 55, 55, 55, 65]
    assert(lowestHigherThanXIndex(50, list) == 2)       
    assert(lowestHigherThanXIndex(55, list) == 2)
    assert(lowestHigherThanXIndex(60, list) == 5)
    list = [15, 18, 55, 55, 55, 65, 90]
    assert(lowestHigherThanXIndex(50, list) == 2)       
    assert(lowestHigherThanXIndex(55, list) == 2)
    assert(lowestHigherThanXIndex(60, list) == 5)

 


if __name__ == '__main__':

    lowestHigherThanIndexTest()

    