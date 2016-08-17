import subprocess
import time

cmd = ['python', '/home/people/krdav/cluster_test_runner.py']
for i in range(56):
    subprocess.Popen(cmd)

# Sleep an hour
time.sleep(60*60)


