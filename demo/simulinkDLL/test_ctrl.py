import os
import sys
import platform
from ctypes import util
from ctypes import *

# noinspection SpellCheckingInspection
uint16_T = c_ushort  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL/rtwtypes.h: 50
# noinspection SpellCheckingInspection
int32_T = c_int  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL/rtwtypes.h: 51
# noinspection SpellCheckingInspection
uint32_T = c_uint  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL/rtwtypes.h: 52
# noinspection SpellCheckingInspection
real32_T = c_float  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL/rtwtypes.h: 53
# noinspection SpellCheckingInspection
real_T = c_double  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL/rtwtypes.h: 60
# noinspection SpellCheckingInspection
boolean_T = c_ubyte  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL/rtwtypes.h: 62


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 127
class struct_tag_RTM_test_ctrl(Structure):
    def __init__(self):
        self.dwork = POINTER(D_Work_test_ctrl)()
        self.test_ctrl_InstP_ref = POINTER(InstP_test_ctrl)()
        super().__init__(
                         dwork=self.dwork,
                         test_ctrl_InstP_ref=self.test_ctrl_InstP_ref,
         )


# noinspection SpellCheckingInspection
RT_MODEL_test_ctrl = struct_tag_RTM_test_ctrl  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 26


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 34
class struct_anon_16(Structure):
    def __init__(self):
        self.diag1 = real32_T(0)
        self.diag2 = False
        super().__init__(
                         diag1=self.diag1,
                         diag2=self.diag2,
         )


struct_anon_16._fields_ = [
    ('diag1', real32_T),
    ('diag2', boolean_T),
]
# noinspection SpellCheckingInspection
TEST_CTRL_D_t = struct_anon_16  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 34


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 44
class struct_anon_17(Structure):
    def __init__(self):
        self.in1 = uint16_T(0)
        self.in2 = int32_T(0)
        super().__init__(
                         in1=self.in1,
                         in2=self.in2,
         )


struct_anon_17._fields_ = [
    ('in1', uint16_T),
    ('in2', int32_T),
]
# noinspection SpellCheckingInspection
InBus_t = struct_anon_17  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 44
# noinspection SpellCheckingInspection
enum_anon_18 = c_int  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
WORK_STATE_STREET = 0  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
WORK_STATE_FIELD = 1  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
WORK_STATE_HEADLAND = 2  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
WORK_STATE_OPEN_A_FIELD = 3  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
WORK_STATE_REVERSING = 4  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
WORK_STATE_ERROR_INDICATION = 14  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
WORK_STATE_NOT_AVAILABLE = 15  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59
# noinspection SpellCheckingInspection
workingStateTypes = enum_anon_18  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 59


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 73
class struct_anon_19(Structure):
    def __init__(self):
        self.input1 = InBus_t()
        self.input2 = int32_T(0)
        self.input3 = real32_T(0)
        self.input4 = real_T(0)
        self.input5 = False
        self.input6 = workingStateTypes()
        super().__init__(
                         input1=self.input1,
                         input2=self.input2,
                         input3=self.input3,
                         input4=self.input4,
                         input5=self.input5,
                         input6=self.input6,
         )


struct_anon_19._fields_ = [
    ('input1', InBus_t),
    ('input2', int32_T),
    ('input3', real32_T),
    ('input4', real_T),
    ('input5', boolean_T),
    ('input6', workingStateTypes),
]
# noinspection SpellCheckingInspection
TEST_CTRL_U_t = struct_anon_19  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 73


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 83
class struct_anon_20(Structure):
    def __init__(self):
        self.output1 = real32_T(0)
        self.output2 = False
        super().__init__(
                         output1=self.output1,
                         output2=self.output2,
         )


struct_anon_20._fields_ = [
    ('output1', real32_T),
    ('output2', boolean_T),
]
# noinspection SpellCheckingInspection
TEST_CTRL_Y_t = struct_anon_20  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 83


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 94
class struct_anon_21(Structure):
    def __init__(self):
        self.ts = uint32_T(0)
        self.para1 = real32_T(0)
        self.para2 = real32_T(0)
        super().__init__(
                         ts=self.ts,
                         para1=self.para1,
                         para2=self.para2,
         )


struct_anon_21._fields_ = [
    ('ts', uint32_T),
    ('para1', real32_T),
    ('para2', real32_T),
]
# noinspection SpellCheckingInspection
TEST_CTRL_P_t = struct_anon_21  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 94


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 103
class struct_anon_22(Structure):
    def __init__(self):
        self.d = TEST_CTRL_D_t()
        self.DiscreteTimeIntegrator_DSTATE = real32_T(0)
        self.UnitDelay_DSTATE = real32_T(0)
        super().__init__(
                         d=self.d,
                         DiscreteTimeIntegrator_DSTATE=self.DiscreteTimeIntegrator_DSTATE,
                         UnitDelay_DSTATE=self.UnitDelay_DSTATE,
         )


struct_anon_22._fields_ = [
    ('d', TEST_CTRL_D_t),
    ('DiscreteTimeIntegrator_DSTATE', real32_T),
    ('UnitDelay_DSTATE', real32_T),
]
# noinspection SpellCheckingInspection
D_Work_test_ctrl = struct_anon_22  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 103


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 113
class struct_anon_23(Structure):
    def __init__(self):
        self.p = TEST_CTRL_P_t()
        super().__init__(
                         p=self.p,
         )


struct_anon_23._fields_ = [
    ('p', TEST_CTRL_P_t),
]
# noinspection SpellCheckingInspection
InstP_test_ctrl = struct_anon_23  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 113


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 118
class struct_anon_24(Structure):
    def __init__(self):
        self.U = TEST_CTRL_U_t()
        super().__init__(
                         U=self.U,
         )


struct_anon_24._fields_ = [
    ('U', TEST_CTRL_U_t),
]
# noinspection SpellCheckingInspection
ExternalInputs_test_ctrl = struct_anon_24  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 118


# noinspection PyPep8Naming
# C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 124
class struct_anon_25(Structure):
    def __init__(self):
        self.Y = TEST_CTRL_Y_t()
        self.D = TEST_CTRL_D_t()
        super().__init__(
                         Y=self.Y,
                         D=self.D,
         )


struct_anon_25._fields_ = [
    ('Y', TEST_CTRL_Y_t),
    ('D', TEST_CTRL_D_t),
]
# noinspection SpellCheckingInspection
ExternalOutputs_test_ctrl = struct_anon_25  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 124
struct_tag_RTM_test_ctrl._fields_ = [
    ('dwork', POINTER(D_Work_test_ctrl)),
    ('test_ctrl_InstP_ref', POINTER(InstP_test_ctrl)),
]
# noinspection SpellCheckingInspection
tag_RTM_test_ctrl = struct_tag_RTM_test_ctrl  # C:\\Prj\\GitHub\\ctypesgen\\demo\\SimulinkDLL\\test_ctrl.h: 127


# noinspection PyPep8Naming
class test_ctrl(object):
    def __init__(self, rel_path=None):
        
        # set relative path string based on passed argument
        if rel_path is not None:
            self.relPath = rel_path
        else:
            self.relPath = './'
        
        # construct absolute library folder path from relative path
        curr_dir = os.path.dirname(__file__)  # current directory
        self.libDir = os.path.abspath(os.path.join(curr_dir, self.relPath))
        
        # helping variables
        self.stepNum = []
        self.curr_dir = os.path.dirname(__file__)
        
        # derive library name from model name and system architecture
        self.libName = 'test_ctrl'
        if platform.system() == 'Windows':
            # extend lib name dependent on architecture flag
            if sys.maxsize > 2 ** 32:
                self.libName = self.libName + '_win64'
            else:
                self.libName = self.libName + '_win32'
            
        # construct library full path
        self.libPath = os.path.join(self.libDir, self.libName)
        # check if the library exists
        self.libPathFound = util.find_library('%s' % self.libPath)
        
        # if found then load the library into memory
        if self.libPathFound:
            try:
                if platform.system() == 'Windows':
                    self.lib = windll.LoadLibrary(self.libPath)
                elif platform.system() == 'Linux':
                    self.lib = cdll.LoadLibrary(self.libPath)
                else:
                    print('System architecture %s is not valid.' % platform.system())
                    sys.exit()
            except OSError:
                print('Unable to load the library %s.' % self.libName)
                sys.exit()
        else:
            print('Unable to find the library on path %s.' % self.libPath)
            sys.exit()
        
        # get model interface data structures
        self.M = RT_MODEL_test_ctrl()
        self.U = ExternalInputs_test_ctrl()
        self.Y = ExternalOutputs_test_ctrl()
        self.P = InstP_test_ctrl()
        self.DWork = D_Work_test_ctrl()
        
        # Model entry point functions
        self._initialize = getattr(self.lib, 'test_ctrl_initialize')
        self._step = getattr(self.lib, 'test_ctrl_step')
        self._terminate = getattr(self.lib, 'test_ctrl_terminate')
        
    def initialize(self):
        """ Initialize the model. Prototype taken from 'ert_main.c' """
        # / * Pack model data into RTM * /
        self.M.dwork = pointer(self.DWork)
        self.M.test_ctrl_InstP_ref = pointer(self.P)
        
        # Initialize model
        self._initialize(self.M, byref(self.U), byref(self.Y))
        self.stepNum = 0
        
    def step(self):
        """ Step through the model. Prototype taken from 'ert_main.c' """
        self._step(self.M, byref(self.U), byref(self.Y))
        self.stepNum += 1
        
    def terminate(self):
        """ Terminate the model. Prototype taken from 'ert_main.c' """
        self._terminate(self.M)
