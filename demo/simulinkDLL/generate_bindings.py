import os
import subprocess

# ctypesgen -lneon /usr/local/include/neon/ne_*.h -o neon.py

mdl_name = 'test_ctrl'  # name of the Simulink model that the library was generated from
curr_dir = os.path.dirname(__file__)  # current directory

# Run an arbitrary system command
cmd = 'ctypesgen '
cmd = cmd + '-l' + os.path.join(curr_dir, mdl_name + '_win64.dll') + ' '
cmd = cmd + os.path.join(curr_dir, mdl_name + '.h') + ' '
cmd = cmd + '--include' + ' ' + 'rtwtypes.h' + ' '
# cmd = cmd + '--no-embed-preamble' + ' '
cmd = cmd + '--allow-gnu-c' + ' '
cmd = cmd + '-I' + curr_dir + ' '
cmd = cmd + '-o' + os.path.join(curr_dir, mdl_name + '.py')
result = subprocess.run(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# Print the stdout and stderr
print(result.stdout)
stderr = result.stderr.decode()
stderr = "\n".join(stderr.splitlines())
print(stderr)