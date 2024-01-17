/*
 * File: ert_main.c
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

#include <stddef.h>
#include <stdio.h>            /* This example main program uses printf/fflush */
#include "test_ctrl.h"                 /* Model header file */

static RT_MODEL_test_ctrl test_ctrl_M_;
static RT_MODEL_test_ctrl *const test_ctrl_MPtr = &test_ctrl_M_;/* Real-time model */
static D_Work_test_ctrl test_ctrl_DWork;/* Observable states */

/* instance parameters */
static InstP_test_ctrl test_ctrl_InstP = {
  /* Variable: p
   * Referenced by:
   *   '<S1>/Gain'
   *   '<S1>/Gain1'
   *   '<S1>/Gain2'
   */
  {
    10U,
    1.0F,
    2.0F
  }
};

static ExternalInputs_test_ctrl test_ctrl_U;/* External inputs */
static ExternalOutputs_test_ctrl test_ctrl_Y;/* External outputs */

/*
 * Associating rt_OneStep with a real-time clock or interrupt service routine
 * is what makes the generated code "real-time".  The function rt_OneStep is
 * always associated with the base rate of the model.  Subrates are managed
 * by the base rate from inside the generated code.  Enabling/disabling
 * interrupts and floating point context switches are target specific.  This
 * example code indicates where these should take place relative to executing
 * the generated code step function.  Overrun behavior should be tailored to
 * your application needs.  This example simply sets an error status in the
 * real-time model and returns from rt_OneStep.
 */
void rt_OneStep(RT_MODEL_test_ctrl *const test_ctrl_M);
void rt_OneStep(RT_MODEL_test_ctrl *const test_ctrl_M)
{
  static boolean_T OverrunFlag = false;

  /* Disable interrupts here */

  /* Check for overrun */
  if (OverrunFlag) {
    return;
  }

  OverrunFlag = true;

  /* Save FPU context here (if necessary) */
  /* Re-enable timer or interrupt here */
  /* Set model inputs here */

  /* Step the model */
  test_ctrl_step(test_ctrl_M, &test_ctrl_U, &test_ctrl_Y);

  /* Get model outputs here */

  /* Indicate task complete */
  OverrunFlag = false;

  /* Disable interrupts here */
  /* Restore FPU context here (if necessary) */
  /* Enable interrupts here */
}

/*
 * The example main function illustrates what is required by your
 * application code to initialize, execute, and terminate the generated code.
 * Attaching rt_OneStep to a real-time clock is target specific. This example
 * illustrates how you do this relative to initializing the model.
 */
int_T main(int_T argc, const char *argv[])
{
  RT_MODEL_test_ctrl *const test_ctrl_M = test_ctrl_MPtr;

  /* Unused arguments */
  (void)(argc);
  (void)(argv);

  /* Pack model data into RTM */
  test_ctrl_M->dwork = &test_ctrl_DWork;
  test_ctrl_M->test_ctrl_InstP_ref = &test_ctrl_InstP;

  /* Initialize model */
  test_ctrl_initialize(test_ctrl_M, &test_ctrl_U, &test_ctrl_Y);

  /* Attach rt_OneStep to a timer or interrupt service routine with
   * period 0.2 seconds (base rate of the model) here.
   * The call syntax for rt_OneStep is
   *
   *  rt_OneStep(test_ctrl_M);
   */
  printf("Warning: The simulation will run forever. "
         "Generated ERT main won't simulate model step behavior. "
         "To change this behavior select the 'MAT-file logging' option.\n");
  fflush((NULL));
  while (1) {
    /*  Perform application tasks here */
  }

  /* The option 'Remove error status field in real-time model data structure'
   * is selected, therefore the following code does not need to execute.
   */

  /* Terminate model */
  test_ctrl_terminate(test_ctrl_M);
  return 0;
}

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
