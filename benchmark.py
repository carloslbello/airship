import time
import subprocess
from scipy.stats.mstats import gmean

def benchmark(command):
    clock = time.time()
    subprocess.call(command)
    return time.time() - clock

def benchmark_multiple(command, times):
    subprocess.call(command)
    results = []
    num = 0
    while num < times:
        results.append(benchmark(command))
        num += 1
    return gmean(results)

interpreters = ['python', 'python3', 'pypy', 'pypy3']

results = []

for interpreter in interpreters:
    subprocess.call(['python', 'test.py'])
    results.append(interpreter + ' time: ' + str(benchmark_multiple([interpreter, 'test/run.py'], 10)))

for result in results:
    print(result)
