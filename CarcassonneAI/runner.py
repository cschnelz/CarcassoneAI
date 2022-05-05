import subprocess
import sys
from tqdm import tqdm

script_name = 'main3.py'
output_prefix = 'MCTS_H-200x500-c3-UCB vs Greedy'
n_iter = 15

for i in tqdm(range(n_iter)):
    output_file = output_prefix + '_' + str(i) + '.txt'
    sys.stdout = open(output_file, 'w')
    subprocess.call(['python3.9', script_name], stdout=sys.stdout, stderr=subprocess.STDOUT)