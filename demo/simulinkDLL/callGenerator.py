import subprocess
import platform
from myGenerator import *


def main(mdl_name: str, cli=False):
    """
    @param mdl_name: name of the Simulink model that the library was generated from
    @param cli: Command Line Interface flag
    @return:
    """

    lib_name = ''

    if mdl_name is not None:
        curr_dir = os.path.dirname(__file__)  # current directory

        if platform.system() == 'Windows':
            lib_name = mdl_name + '_win64.dll'
        elif platform.system() == 'Linux':
            lib_name = mdl_name + '.so'

        # Build an arbitrary system command
        cmd = ''
        cmd = cmd + '-l' + os.path.join(curr_dir, lib_name) + ' '
        cmd = cmd + '%s.h' % os.path.join(curr_dir, mdl_name) + ' '
        cmd = cmd + '--include' + ' ' + 'rtwtypes.h' + ' '
        # cmd = cmd + '--no-embed-preamble' + ' '
        cmd = cmd + '--allow-gnu-c' + ' '
        cmd = cmd + '-I' + curr_dir + ' '
        cmd = cmd + '-o' + os.path.join(curr_dir, mdl_name + '.py')

        if cli:
            result = subprocess.run(('ctypesgen ' + cmd).split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # Print the stdout and stderr
            print(result.stdout)
            stderr = result.stderr.decode()
            stderr = "\n".join(stderr.splitlines())
            print(stderr)
        else:
            gen = MyGenerator(given_args=cmd.split(' '))
            gen.main()


if __name__ == '__main__':
    # mdl_name - name of the Simulink model that the library was generated from
    # cli - Command Line Interface
    main(mdl_name='test_ctrl', cli=False)
