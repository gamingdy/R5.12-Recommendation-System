from utils import efficacite
from multiprocessing.pool import Pool
import matplotlib.pyplot as plt
import openpyxl
import os
import time

if __name__ == "__main__":
    nb_user = range(5,19)
    t1 = time.time()
    with Pool() as pool:
        res = pool.map(efficacite, nb_user)

    for res_abs,user_id in res:
        print(res_abs ,"  nb -----  " ,user_id, ": res abs")
    
