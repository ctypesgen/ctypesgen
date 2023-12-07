import sys
import os
from pathlib import Path
from ctypesgen.ctypedescs import CtypesBitfield
from ctypesgen.messages import status_message

from ctypesgen.printer_python.printer import WrapperPrinter


class MyPrinter(WrapperPrinter):
    def __init__(self, out_path, options, data):
        status_message("Writing to %s." % (out_path or "stdout"))
        self.file = open(out_path, "w") if out_path else sys.stdout
        self.out_path = out_path
        self.print_imports()
        # super().__init__(outpath=out_path, options=options, data=data)

        self.out_path = out_path
        self.options = options
        self.data = data
        self.mdlName = Path(data.headers[0]).stem

        method_table = {
            "function": self.print_function,
            "macro": self.print_macro,
            "struct": self.print_struct,
            "struct-body": self.print_struct_members,
            "typedef": self.print_typedef,
            "variable": self.print_variable,
            "enum": self.print_enum,
            "constant": self.print_constant,
            "undef": self.print_undef,
        }

        for kind, desc in data.output_order:
            if desc.included:
                method_table[kind](desc)
                # self.file.write("\n")

        self.print_model()

    def __del__(self):
        if not self.file.closed:
            self.file.close()

    def print_model(self):
        self.file.write("\n\n")
        self.file.write("# noinspection PyPep8Naming\n")
        self.file.write("class %s(object):\n" % self.mdlName)
        self.file.write("    def __init__(self, rel_path=None):\n")
        self.file.write("        \n")
        self.file.write("        # set relative path string based on passed argument\n")
        self.file.write("        if rel_path is not None:\n")
        self.file.write("            self.relPath = rel_path\n")
        self.file.write("        else:\n")
        self.file.write("            self.relPath = './'\n")
        self.file.write("        \n")
        self.file.write("        # construct absolute library folder path from relative path\n")
        self.file.write("        curr_dir = os.path.dirname(__file__)  # current directory\n")
        self.file.write("        self.libDir = os.path.abspath(os.path.join(curr_dir, self.relPath))\n")
        self.file.write("        \n")
        self.file.write("        # helping variables\n")
        self.file.write("        self.stepNum = []\n")
        self.file.write("        self.curr_dir = os.path.dirname(__file__)\n")
        self.file.write("        \n")
        self.file.write("        # derive library name from model name and system architecture\n")
        self.file.write("        self.libName = '%s'\n" % self.mdlName)
        self.file.write("        if platform.system() == 'Windows':\n")
        self.file.write("            # extend lib name dependent on architecture flag\n")
        self.file.write("            if sys.maxsize > 2 ** 32:\n")
        self.file.write("                self.libName = self.libName + '_win64'\n")
        self.file.write("            else:\n")
        self.file.write("                self.libName = self.libName + '_win32'\n")
        self.file.write("            \n")
        self.file.write("        # construct library full path\n")
        self.file.write("        self.libPath = os.path.join(self.libDir, self.libName)\n")
        self.file.write("        # check if the library exists\n")
        self.file.write("        self.libPathFound = util.find_library('%s' % self.libPath)\n")
        self.file.write("        \n")
        self.file.write("        # if found then load the library into memory\n")
        self.file.write("        if self.libPathFound:\n")
        self.file.write("            try:\n")
        self.file.write("                if platform.system() == 'Windows':\n")
        self.file.write("                    self.lib = windll.LoadLibrary(self.libPath)\n")
        self.file.write("                elif platform.system() == 'Linux':\n")
        self.file.write("                    self.lib = cdll.LoadLibrary(self.libPath)\n")
        self.file.write("                else:\n")
        self.file.write("                    print('System architecture "'%s'" is not valid.' % platform.system())\n")
        self.file.write("                    sys.exit()\n")
        self.file.write("            except OSError:\n")
        self.file.write("                print('Unable to load the library "'%s'".' % self.libName)\n")
        self.file.write("                sys.exit()\n")
        self.file.write("        else:\n")
        self.file.write("            print('Unable to find the library on path "'%s'".' % self.libPath)\n")
        self.file.write("            sys.exit()\n")
        self.file.write("        \n")
        self.file.write("        # get model interface data structures\n")
        self.file.write("        self.M = RT_MODEL_%s()\n" % self.mdlName)
        self.file.write("        self.U = ExternalInputs_%s()\n" % self.mdlName)
        self.file.write("        self.Y = ExternalOutputs_%s()\n" % self.mdlName)
        self.file.write("        self.P = InstP_%s()\n" % self.mdlName)
        self.file.write("        self.DWork = D_Work_%s()\n" % self.mdlName)
        self.file.write("        \n")
        self.file.write("        # Model entry point functions\n")
        self.file.write("        self._initialize = getattr(self.lib, '%s_initialize')\n" % self.mdlName)
        self.file.write("        self._step = getattr(self.lib, '%s_step')\n" % self.mdlName)
        self.file.write("        self._terminate = getattr(self.lib, '%s_terminate')\n" % self.mdlName)
        self.file.write("        \n")
        self.file.write("    def initialize(self):\n")
        self.file.write("        %s%s%s Initialize the model. Prototype taken from 'ert_main.c' %s%s%s\n"
                        % (f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}'))
        self.file.write("        # / * Pack model data into RTM * /\n")
        self.file.write("        self.M.dwork = pointer(self.DWork)\n")
        self.file.write("        self.M.%s_InstP_ref = pointer(self.P)\n" % self.mdlName)
        self.file.write("        \n")
        self.file.write("        # Initialize model\n")
        self.file.write("        self._initialize(self.M, byref(self.U), byref(self.Y))\n")
        self.file.write("        self.stepNum = 0\n")
        self.file.write("        \n")
        self.file.write("    def step(self):\n")
        self.file.write("        %s%s%s Step through the model. Prototype taken from 'ert_main.c' %s%s%s\n"
                        % (f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}'))
        self.file.write("        self._step(self.M, byref(self.U), byref(self.Y))\n")
        self.file.write("        self.stepNum += 1\n")
        self.file.write("        \n")
        self.file.write("    def terminate(self):\n")
        self.file.write("        %s%s%s Terminate the model. Prototype taken from 'ert_main.c' %s%s%s\n"
                        % (f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}', f'{chr(34)}'))
        self.file.write("        self._terminate(self.M)\n")

    def print_imports(self):
        self.file.write("import os\n")
        self.file.write("import sys\n")
        self.file.write("import platform\n")
        self.file.write("from ctypes import util\n")
        self.file.write("from ctypes import *\n\n")

    def print_typedef(self, typedef):
        self.file.write("# noinspection SpellCheckingInspection\n")
        self.file.write("%s = %s  " % (typedef.name, typedef.ctype.py_string()))
        self.srcinfo(typedef.src)

    def print_enum(self, enum):
        self.file.write("# noinspection SpellCheckingInspection\n")
        self.file.write("enum_%s = c_int  " % enum.tag)
        self.srcinfo(enum.src)
        # Values of enumerator are output as constants.
        # ToDo: combine separated values to an Enum class
        # dep = next(iter(enum.dependents))
        # self.file.write("class %s(Enum):\n" % dep.name)
        # for string, node in enum.members:
        #     self.file.write("    %s = %d\n" % (string, node.value))


    def print_constant(self, constant):
        self.file.write("%s = %s  " % (constant.name, constant.value.py_string(False)))
        self.srcinfo(constant.src)

    def srcinfo(self, src):
        if src is None:
            pass
            # self.file.write("\n")
        else:
            filename, lineno = src
            if filename in ("<built-in>", "<command line>"):
                self.file.write("# %s\n" % filename)
            else:
                if self.options.strip_build_path and filename.startswith(self.options.strip_build_path):
                    filename = filename[len(self.options.strip_build_path):]
                self.file.write("# %s: %s\n" % (filename, lineno))

    def print_group(self, _list, name, function):
        pass

    def print_struct_members(self, struct):
        if struct.opaque:
            return

        self.file.write("%s_%s._fields_ = [\n" % (struct.variety, struct.tag))
        for name, cType in struct.members:
            if isinstance(cType, CtypesBitfield):
                self.file.write(
                    "    ('%s', %s, %s),\n"
                    % (name, cType.py_string(), cType.bitfield.py_string(False))
                )
            else:
                self.file.write("    ('%s', %s),\n" % (name, cType.py_string()))
        self.file.write("]\n")

    def print_struct(self, struct):
        self.file.write("\n\n")
        self.file.write("# noinspection PyPep8Naming\n")
        self.srcinfo(struct.src)
        base = {"union": "Union", "struct": "Structure"}[struct.variety]
        self.file.write("class %s_%s(%s):\n" "    def __init__(self):\n" % (struct.variety, struct.tag, base))
        for name, cType in struct.members:
            if isinstance(cType, CtypesBitfield):
                self.file.write("        self.%s = %s\n" % (name, cType.bitfield.py_string(False)))
            elif hasattr(cType, 'name'):
                if getattr(cType, 'name') == 'boolean_T':
                    self.file.write("        self.%s = %s\n" % (name, 'False'))
                elif ((getattr(cType, 'name') == 'uint_T') or
                      (getattr(cType, 'name') == 'int_T') or
                      (getattr(cType, 'name') == 'real_T') or
                      (getattr(cType, 'name') == 'uint8_T') or
                      (getattr(cType, 'name') == 'int8_T') or
                      (getattr(cType, 'name') == 'uint16_T') or
                      (getattr(cType, 'name') == 'int16_T') or
                      (getattr(cType, 'name') == 'uint32_T') or
                      (getattr(cType, 'name') == 'int32_T') or
                      (getattr(cType, 'name') == 'real32_T') or
                      (getattr(cType, 'name') == 'uint64_T') or
                      (getattr(cType, 'name') == 'int64_T') or
                      (getattr(cType, 'name') == 'real64_T')):
                    self.file.write("        self.%s = %s(%d)\n" % (name, cType.py_string(), 0))
                else:
                    self.file.write("        self.%s = %s()\n" % (name, cType.py_string()))
            else:
                self.file.write("        self.%s = %s()\n" % (name, cType.py_string()))
        self.file.write("        super().__init__(\n")

        for name, cType in struct.members:
            self.file.write("                         %s=self.%s,\n" % (name, name))
        self.file.write("         )\n")
        # self.file.write("    pass\n")
        self.file.write("\n\n")

    def template_subs(self):
        pass

    def print_header(self):
        pass

    def print_preamble(self):
        pass

    def _copy_preamble_loader_files(self, path):
        pass

    def print_loader(self):
        pass

    def print_library(self, library):
        pass

    def print_function(self, function):
        pass

    def print_fixed_function(self, function):
        pass

    def print_variadic_function(self, function):
        pass

    def print_variable(self, variable):
        pass

    def print_macro(self, macro):
        pass

    def print_simple_macro(self, macro):
        pass

    def print_func_macro(self, macro):
        pass

    def strip_prefixes(self):
        pass

    def insert_file(self, filename):
        pass
