import random
import string
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    
    randomList="list"
    r=0
    # traversing the loop 15 times
    for x in range(size) :
      r+=random.choice(chars)
    
    return r
 
# function call for random string
# generation with size 8 and string
print (ran_gen(8, "AEIOSUMA23"))