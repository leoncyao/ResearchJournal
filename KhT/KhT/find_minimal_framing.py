import sys
import os
from BNComplexes import *
from CobComplexes import *
from Drawing import *
from CrossingTangle import *

import KhT
import ConcatWebpages

# goal, find the number integer describing number of twists to do to tangle, such that the tail of 
# the arc invariant chain complex dissapears

# first calculate chain complex with no twists, see how many black dots "n" at the end of the complex
# (this is mainly to check my work)
# for i in range(-10, 10):
#   calculate chain complex for tangle with i twists at bottom
#   check that the number of blacks dots becomes 0 
def main(name, tangle_path=None, resultingdirectory=None):
    print("------------------------------------------------------")
    print("STARTING SMALL ARC CALCULATION")
    print("------------------------------------------------------")
    tangle_path_str = "../examples/"
    if tangle_path:
        tangle_path_str += tangle_path
    else:
        tangle_path_str += "miscellaneous"
    tangle_path_str += "/"
    f = open(tangle_path_str + name + ".txt", "r")
    # print(tangle_path_str + name + ".txt")
    tangle_str = f.read()
    # print("tangle_str: " + tangle_str)
    
    cx = BNbracket(tangle_str,0,0,1) # compute Bar-Natan's bracket
    BNr = cx.ToBNAlgebra(2) # convert the Bar-Natan's bracket into a complex over BNAlgebra
    BNr.eliminateAll() # cancel all identity components of the differential
    BNr.clean_up() # try to find the immersed curve invariant BNr through a sequence of random isotopies
    multicurve = BNr.to_multicurve()


    k = 0
    if name == "asimov_2":
        return 0
        # k = 1

    # assuming arc invariant has only one comp
    order = multicurve.comps[k].gens

    for gen in order:
        print(gen.h)

    # need to figure out whether the last connected component is increasing or decreasing (and the list is reversed)

    # flag == true implies the last chain is increasing, false means decreasing
    flag = order[0].h <= order[1].h

    print("flag is " + str(flag))
    KhT.asdf(name, tangle_path=tangle_path, resultingdirectory=name)

    # tries = [0] + [(-1)**(i) * int((i)/2) for i in range(2, 20)]
    tries = [(-1)**(i) * int((i)/2) for i in range(2, 20)]
    for i in tries:
        if i > 0:
            new_tangle_str = tangle_str + ".pos0" * i
        else:
            new_tangle_str = tangle_str + ".neg0" * abs(i)

        # Tangle = Tangle(new_tangle)
        # print("test" + new_tangle_str)
        cx = BNbracket(new_tangle_str,0,0,1) # compute Bar-Natan's bracket
        BNr = cx.ToBNAlgebra(2) # convert the Bar-Natan's bracket into a complex over BNAlgebra
        BNr.eliminateAll() # cancel all identity components of the differential
        # print(BNr)
        BNr.clean_up() # try to find the immersed curve invariant BNr through a sequence of random isotopies
        #BNr.draw(name)
        multicurve = BNr.to_multicurve()

        # assuming arc invariant has only one comp
        order = multicurve.comps[k].gens
        
        # for gen in order:
        #     print(gen.h)
        # print(order[0].h)
        # print(order[1].h)
        print(i)
        if not (order[0].h <= order[1].h)  == flag :    
            print("FOUND SMALL ARC")
            for gen in order:
                print(gen.h)
            
            new_name = name + "_minimal" 
            f = open(tangle_path_str + new_name + ".txt", "w+")

            # want to start are on a white dot
            f.write(new_tangle_str)
            # f.write(new_tangle_str[:-5])
            f.close()
            print("tangle path is " + tangle_path)
            print("resulting directory is " + str(resultingdirectory))
            
            KhT.asdf(new_name, tangle_path=tangle_path, resultingdirectory=name)
            break
        
        # new_name = name + "_" + str(i) + "_minimal" 
        # f = open(tangle_path_str + new_name + ".txt", "w+")
        # # f.write(new_tangle_str)
        # f.write(new_tangle_str[:-5])
        # f.close()
        # KhT.asdf(new_name, tangle_path=tangle_path, resultingdirectory=resultingdirectory)

    ConcatWebpages.main(name)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
# if __name__ == "__main__":
    # name = sys.argv[1]
    # tangle_path = "../examples/"
    # if len(sys.argv) > 3:
    #     tangle_path += sys.argv[3]
    # else:
    #     tangle_path += "miscellaneous"
    # # f = open(name + ".txt", "r")
    # tangle_path += "/"
    # f = open(tangle_path + name + ".txt", "r")
    # tangle_str = f.read()
    # tries = [0] + [(-1)**(i) * int((i)/2) for i in range(2, 50)]
    # for i in tries:
    #     if i > 0:
    #         new_tangle_str = tangle_str + ".pos0" * i
    #     else:
    #         new_tangle_str = tangle_str + ".neg0" * abs(i)

    #     # Tangle = Tangle(new_tangle)
    #     cx = BNbracket(new_tangle_str,0,0,1) # compute Bar-Natan's bracket
    #     BNr = cx.ToBNAlgebra(2) # convert the Bar-Natan's bracket into a complex over BNAlgebra
    #     BNr.eliminateAll() # cancel all identity components of the differential
    #     # print(BNr)
    #     BNr.clean_up() # try to find the immersed curve invariant BNr through a sequence of random isotopies
    #     #BNr.draw(name)
    #     multicurve = BNr.to_multicurve()

    #     # assuming has one comp
    #     order = multicurve.comps[0].gens
    #     if order[0].h <= order[1].h:    
    #         new_name = name + "_minimal"
    #         f = open(tangle_path + new_name + ".txt", "w+")
    #         # print("truncated str is " + new_tangle_str[:-5])
    #         # print(f)
    #         f.write(new_tangle_str[:-5])
    #         f.close()
    #         print("check" + sys.argv[1])
    #         if len(sys.argv) == 2:
    #             KhT.asdf(new_name)
    #         if len(sys.argv) == 3:
    #             KhT.asdf(new_name, resultingdirectory=sys.argv[2])
    #         if len(sys.argv) == 4:
    #             KhT.asdf(new_name, tanglepath=sys.argv[2], resultingdirectory=sys.argv[3])
    #         break
        

