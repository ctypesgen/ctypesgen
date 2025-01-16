/*
 * File: test_ctrl.c
 *
 * Code generated for Simulink model 'test_ctrl'.
 *
 * Model version                  : 5.10
 * Simulink Coder version         : 23.2 (R2023b) 01-Aug-2023
 * C/C++ source code generated on : Tue Dec  5 22:49:52 2023
 *
 * Target selection: ert_shrlib.tlc
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include "test_ctrl.h"
#include "rtwtypes.h"
#include <string.h>

const TEST_CTRL_U_t test_ctrl_rtZTEST_CTRL_U_t = { { 0U,/* in1 */
    0                                  /* in2 */
  },                                   /* input1 */
  0,                                   /* input2 */
  0.0F,                                /* input3 */
  0.0,                                 /* input4 */
  false,                               /* input5 */
  WORK_STATE_NOT_AVAILABLE             /* input6 */
};

/*===========*
 * Constants *
 *===========*/
#define RT_PI                          3.14159265358979323846
#define RT_PIF                         3.1415927F
#define RT_LN_10                       2.30258509299404568402
#define RT_LN_10F                      2.3025851F
#define RT_LOG10E                      0.43429448190325182765
#define RT_LOG10EF                     0.43429449F
#define RT_E                           2.7182818284590452354
#define RT_EF                          2.7182817F

/*
 * UNUSED_PARAMETER(x)
 *   Used to specify that a function parameter (argument) is required but not
 *   accessed by the function body.
 */
#ifndef UNUSED_PARAMETER
#if defined(__LCC__)
#define UNUSED_PARAMETER(x)                                      /* do nothing */
#else

/*
 * This is the semi-ANSI standard way of indicating that an
 * unused function parameter is required.
 */
#define UNUSED_PARAMETER(x)            (void) (x)
#endif
#endif

/* Model step function */
void test_ctrl_step(RT_MODEL_test_ctrl *const test_ctrl_M,
                    ExternalInputs_test_ctrl *test_ctrl_U,
                    ExternalOutputs_test_ctrl *test_ctrl_Y)
{
  D_Work_test_ctrl *test_ctrl_DWork = test_ctrl_M->dwork;
  InstP_test_ctrl *test_ctrl_InstP = test_ctrl_M->test_ctrl_InstP_ref;

  /* Outputs for Atomic SubSystem: '<Root>/fan_fcn' */
  /* Gain: '<S1>/Gain2' incorporates:
   *  DataStoreWrite: '<S1>/Data Store Write'
   */
  test_ctrl_DWork->d.diag1 = test_ctrl_InstP->p.para2 * (real32_T)
    test_ctrl_U->U.input2;

  /* RelationalOperator: '<S1>/GreaterThan1' incorporates:
   *  Constant: '<S1>/Constant2'
   *  DataStoreWrite: '<S1>/Data Store Write'
   */
  test_ctrl_DWork->d.diag2 = (test_ctrl_U->U.input6 == WORK_STATE_FIELD);

  /* RelationalOperator: '<S1>/GreaterThan' incorporates:
   *  Constant: '<S1>/Constant1'
   *  DiscreteIntegrator: '<S1>/Discrete-Time Integrator'
   */
  test_ctrl_Y->Y.output2 = (test_ctrl_DWork->DiscreteTimeIntegrator_DSTATE >
    10.0F);

  /* BusCreator: '<S1>/Bus Creator' incorporates:
   *  DiscreteIntegrator: '<S1>/Discrete-Time Integrator'
   *  Outport: '<Root>/Y'
   */
  test_ctrl_Y->Y.output1 = test_ctrl_DWork->DiscreteTimeIntegrator_DSTATE;

  /* Gain: '<S1>/Gain1' incorporates:
   *  Gain: '<S1>/Gain'
   *  Product: '<S1>/Product'
   *  UnitDelay: '<S1>/Unit Delay'
   */
  test_ctrl_DWork->UnitDelay_DSTATE = test_ctrl_InstP->p.para1 * (real32_T)
    test_ctrl_U->U.input1.in1 * test_ctrl_DWork->UnitDelay_DSTATE * (real32_T)
    test_ctrl_InstP->p.ts;

  /* Update for DiscreteIntegrator: '<S1>/Discrete-Time Integrator' incorporates:
   *  Gain: '<S1>/Gain3'
   *  UnitDelay: '<S1>/Unit Delay'
   */
  test_ctrl_DWork->DiscreteTimeIntegrator_DSTATE += 0.001F *
    test_ctrl_DWork->UnitDelay_DSTATE;

  /* Update for UnitDelay: '<S1>/Unit Delay' */
  test_ctrl_DWork->UnitDelay_DSTATE = test_ctrl_U->U.input3;

  /* End of Outputs for SubSystem: '<Root>/fan_fcn' */

  /* Outport: '<Root>/D' incorporates:
   *  DataStoreRead: '<Root>/Data Store Read'
   */
  test_ctrl_Y->D = test_ctrl_DWork->d;
}

/* Model initialize function */
void test_ctrl_initialize(RT_MODEL_test_ctrl *const test_ctrl_M,
  ExternalInputs_test_ctrl *test_ctrl_U, ExternalOutputs_test_ctrl *test_ctrl_Y)
{
  D_Work_test_ctrl *test_ctrl_DWork = test_ctrl_M->dwork;

  /* Registration code */

  /* states (dwork) */
  (void) memset((void *)test_ctrl_DWork, 0,
                sizeof(D_Work_test_ctrl));

  /* external inputs */
  test_ctrl_U->U = test_ctrl_rtZTEST_CTRL_U_t;

  /* external outputs */
  (void)memset(test_ctrl_Y, 0, sizeof(ExternalOutputs_test_ctrl));
}

/* Model terminate function */
void test_ctrl_terminate(RT_MODEL_test_ctrl *const test_ctrl_M)
{
  /* (no terminate code required) */
  UNUSED_PARAMETER(test_ctrl_M);
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
