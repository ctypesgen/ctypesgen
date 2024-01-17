/*
 * File: test_ctrl.h
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

#ifndef RTW_HEADER_test_ctrl_h_
#define RTW_HEADER_test_ctrl_h_
#ifndef test_ctrl_COMMON_INCLUDES_
#define test_ctrl_COMMON_INCLUDES_
#include "rtwtypes.h"
#endif                                 /* test_ctrl_COMMON_INCLUDES_ */

#include <string.h>

/* Forward declaration for rtModel */
typedef struct tag_RTM_test_ctrl RT_MODEL_test_ctrl;

#ifndef DEFINED_TYPEDEF_FOR_TEST_CTRL_D_t_
#define DEFINED_TYPEDEF_FOR_TEST_CTRL_D_t_

typedef struct {
  real32_T diag1;
  boolean_T diag2;
} TEST_CTRL_D_t;

#endif

#ifndef DEFINED_TYPEDEF_FOR_InBus_t_
#define DEFINED_TYPEDEF_FOR_InBus_t_

typedef struct {
  uint16_T in1;
  int32_T in2;
} InBus_t;

#endif

#ifndef DEFINED_TYPEDEF_FOR_workingStateTypes_
#define DEFINED_TYPEDEF_FOR_workingStateTypes_

typedef enum {
  WORK_STATE_STREET = 0,
  WORK_STATE_FIELD = 1,
  WORK_STATE_HEADLAND = 2,
  WORK_STATE_OPEN_A_FIELD = 3,
  WORK_STATE_REVERSING = 4,
  WORK_STATE_ERROR_INDICATION = 14,
  WORK_STATE_NOT_AVAILABLE = 15        /* Default value */
} workingStateTypes;

#endif

#ifndef DEFINED_TYPEDEF_FOR_TEST_CTRL_U_t_
#define DEFINED_TYPEDEF_FOR_TEST_CTRL_U_t_

typedef struct {
  InBus_t input1;
  int32_T input2;
  real32_T input3;
  real_T input4;
  boolean_T input5;
  workingStateTypes input6;
} TEST_CTRL_U_t;

#endif

#ifndef DEFINED_TYPEDEF_FOR_TEST_CTRL_Y_t_
#define DEFINED_TYPEDEF_FOR_TEST_CTRL_Y_t_

typedef struct {
  real32_T output1;
  boolean_T output2;
} TEST_CTRL_Y_t;

#endif

#ifndef DEFINED_TYPEDEF_FOR_TEST_CTRL_P_t_
#define DEFINED_TYPEDEF_FOR_TEST_CTRL_P_t_

typedef struct {
  uint32_T ts;
  real32_T para1;
  real32_T para2;
} TEST_CTRL_P_t;

#endif

/* Block states (default storage) for system '<Root>' */
typedef struct {
  TEST_CTRL_D_t d;                     /* '<Root>/diag' */
  real32_T DiscreteTimeIntegrator_DSTATE;/* '<S1>/Discrete-Time Integrator' */
  real32_T UnitDelay_DSTATE;           /* '<S1>/Unit Delay' */
} D_Work_test_ctrl;

/* instance parameters, for system '<Root>' */
typedef struct {
  TEST_CTRL_P_t p;                     /* Variable: p
                                        * Referenced by:
                                        *   '<S1>/Gain'
                                        *   '<S1>/Gain1'
                                        *   '<S1>/Gain2'
                                        */
} InstP_test_ctrl;

/* External inputs (root inport signals with default storage) */
typedef struct {
  TEST_CTRL_U_t U;                     /* '<Root>/U' */
} ExternalInputs_test_ctrl;

/* External outputs (root outports fed by signals with default storage) */
typedef struct {
  TEST_CTRL_Y_t Y;                     /* '<Root>/Y' */
  TEST_CTRL_D_t D;                     /* '<Root>/D' */
} ExternalOutputs_test_ctrl;

/* Real-time Model Data Structure */
struct tag_RTM_test_ctrl {
  D_Work_test_ctrl *dwork;
  InstP_test_ctrl *test_ctrl_InstP_ref;
};

/* External data declarations for dependent source files */
extern const TEST_CTRL_U_t test_ctrl_rtZTEST_CTRL_U_t;/* TEST_CTRL_U_t ground */

/* Model entry point functions */
extern void test_ctrl_initialize(RT_MODEL_test_ctrl *const test_ctrl_M,
  ExternalInputs_test_ctrl *test_ctrl_U, ExternalOutputs_test_ctrl *test_ctrl_Y);
extern void test_ctrl_step(RT_MODEL_test_ctrl *const test_ctrl_M,
  ExternalInputs_test_ctrl *test_ctrl_U, ExternalOutputs_test_ctrl *test_ctrl_Y);
extern void test_ctrl_terminate(RT_MODEL_test_ctrl *const test_ctrl_M);

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Use the MATLAB hilite_system command to trace the generated code back
 * to the model.  For example,
 *
 * hilite_system('<S3>')    - opens system 3
 * hilite_system('<S3>/Kp') - opens and selects block Kp which resides in S3
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'test_ctrl'
 * '<S1>'   : 'test_ctrl/fan_fcn'
 */
#endif                                 /* RTW_HEADER_test_ctrl_h_ */

/*
 * File trailer for generated code.
 *
 * [EOF]
 */
