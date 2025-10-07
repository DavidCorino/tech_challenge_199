import time
import pandas as pd

def display(obj):
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        print(obj.to_string())
    else:
        print(obj)

def start_timer():
    return time.time()

def end_timer(t0):
    t1 = time.time()
    total = t1 - t0
    m, s = divmod(total, 60)
    print("\nTempo total de execução do código:")
    print(f"{int(m)} minutos e {int(s)} segundos")

