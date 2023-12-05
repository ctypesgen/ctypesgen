from test_ctrl import *
from ctypes import *


class Model(object):
    def __init__(self, model=None, ts=None):
        if ts is not None:
            self.model = model
        else:
            self.model = None

        if ts is not None:
            self.ts = ts
        else:
            self.ts = 1  # 1 msec

        self.step_num = 0

        ########################################################################
        # using eval is uncool because loosing struct intellisense             #
        self.M = RT_MODEL_test_ctrl()  # replace model name if needed          #
        self.U = ExternalInputs_test_ctrl()  # replace model name if needed    #
        self.Y = ExternalOutputs_test_ctrl()  # replace model name if needed   #
        self.P = InstP_test_ctrl()  # replace model name if needed             #
        self.DWork = D_Work_test_ctrl()  # replace model name if needed        #
        ########################################################################

        # load the library into memory
        # consider only windows x64 dll with '_win64' ending in the current folder
        self.lib_path = ctypes.util.find_library("./%s_win64" % self.model)
        if not self.lib_path:
            print("Unable to find the specified library.")
            sys.exit()
        try:
            if platform.system() == "Windows":
                self.lib = ctypes.windll.LoadLibrary(self.lib_path)
            elif platform.system() == "Linux":
                self.lib = ctypes.cdll.LoadLibrary(self.lib_path)
        except OSError:
            print("Unable to load the system C library")
            sys.exit()

        # Model entry point functions
        self._initialize = getattr(self.lib, r"%s_initialize" % self.model)
        self._step = getattr(self.lib, r"%s_step" % self.model)
        self._terminate = getattr(self.lib, r"%s_terminate" % self.model)

    def initialize(self):
        """ Initialize the model. Prototype taken from 'ert_main.c' """
        # / * Pack model data into RTM * /
        self.M.dwork = pointer(self.DWork)
        self.M.test_ctrl_InstP_ref = pointer(self.P)

        # self.P.contents = [20, 2, 4]
        self.P.p.ts = uint32_T(self.ts)
        self._initialize(self.M, byref(self.U), byref(self.Y))
        self.step_num = -1

    def step(self):
        """ Step through the model. Prototype taken from 'ert_main.c' """
        self._step(self.M, byref(self.U), byref(self.Y))
        self.step_num += 1

    def terminate(self):
        """ Terminate the model. Prototype taken from 'ert_main.c' """
        self._terminate(self.M)


if __name__ == '__main__':
    # get the model class with all necessary wrappers
    sampleTime = 200  # msec
    mdl = Model(model='test_ctrl', ts=sampleTime)

    # initialize I/O structs
    mdl.initialize()

    # set parameter
    mdl.P.p.para1 = real32_T(1.0)
    mdl.P.p.para2 = real32_T(2.0)

    tStop = 0.8  # duration of simulation run in [s]

    # iterate dynamic model
    for i in range(int(tStop/(1e-3*sampleTime))+1):
        elapsedTime = 1e-3*i*sampleTime
        # set inputs
        input1 = InBus_t()
        input1.in1 = uint16_T(1)
        input1.in2 = int32_T(2)
        mdl.U.U.input1 = input1  # nested structure
        mdl.U.U.input2 = int32_T(3)
        mdl.U.U.input3 = real32_T(5.0)

        if elapsedTime > 0.2:
            mdl.U.U.input2 = int32_T(6)
            mdl.U.U.input6 = WORK_STATE_FIELD  # enumeration

        # step the model
        mdl.step()

        # get outputs
        print("time = %0.2f s; output1 = %0.2f; output2 = %s; diag1 = %s; diag2 = %s"
              % (elapsedTime, mdl.Y.Y.output1, mdl.Y.Y.output2, mdl.Y.D.diag1, mdl.Y.D.diag2))

    # terminate the model
    mdl.terminate()
