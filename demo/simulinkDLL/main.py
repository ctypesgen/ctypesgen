import callGenerator
from test_ctrl import *  # """ <- replace model name if needed

if __name__ == '__main__':

    # (re) generate bindings if needed
    # callGenerator.main(mdl_name='test_ctrl', cli=False)

    # get the model class with all necessary wrappers.
    # if no relative path given, model's directory will be searched
    mdl = test_ctrl(rel_path='')  # <- replace model name if needed

    # define sample time im [ms]
    sampleTime = 200

    # set model parameter
    mdl.P.p.ts = uint32_T(sampleTime)
    mdl.P.p.para1 = real32_T(1.0)
    mdl.P.p.para2 = real32_T(2.0)

    # initialize model's internal and interface data
    mdl.initialize()

    tStop = 0.8  # duration of simulation run in [s]
    nSteps = int(tStop/(1e-3*sampleTime))+1

    # iterate dynamic model
    for i in range(nSteps):
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
