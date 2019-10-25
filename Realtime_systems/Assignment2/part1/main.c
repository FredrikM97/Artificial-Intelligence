#include "stdlib.h"
#include "stdio.h"
#include "TaylorSeries.h"
#include "assert.h"
#include "string.h"
#include "time.h"
#include "limits.h"
#include <CUnit/Basic.h>
//#include "CUnit/CUnit.h"


void test_random(void){ //try to break iexp
	srand(time(0));
	int i;
	ExpStruct* test;

	for(i = 0; i < 1000;i++){ //test random int
		test = iexp((rand()%21));
		CU_ASSERT(NULL != test);
		free(test);
	}
}
void test_min(void){
	ExpStruct* test;
	test = iexp(-22); //test min int
	CU_ASSERT(NULL != test);
	CU_ASSERT(150135344 == test->expInt);
	CU_ASSERT(0 == test->expFraction);
	free(test);
}
void test_max(void){
	ExpStruct* test;
	test = iexp(22);//test max int
	CU_ASSERT(NULL != test);
	CU_ASSERT(1994556672 == test->expInt);
	CU_ASSERT(0 == test->expFraction);
	free(test);
}
void test_zero(void){
	ExpStruct* test;
	test = iexp(0);
	CU_ASSERT(NULL != test);
	CU_ASSERT(1 == test->expInt);
	CU_ASSERT(0 == test->expFraction);
	free(test);
}

int main (){
	printf("Start stuff");
	CU_pSuite pSuite = NULL;

	if (CUE_SUCCESS != CU_initialize_registry())
		return CU_get_error();

	pSuite = CU_add_suite("test_expFraction",0,0);
	if (NULL == pSuite) {
      return CU_get_error();
  }
	if(NULL == CU_add_test(pSuite, "test min value",test_min)||
	NULL == CU_add_test(pSuite, "test max value",test_max)||
	NULL == CU_add_test(pSuite, "test zero value",test_zero)||
	NULL == CU_add_test(pSuite, "test random value",test_random)){
		CU_cleanup_registry();
  	return CU_get_error();
	}

	CU_basic_set_mode(CU_BRM_VERBOSE);
	CU_basic_run_tests();
	CU_cleanup_registry();
	return CU_get_error();
/**
g++ *.c -lm -lcunit -o Program
gcc *.c -lm -lcunit -o Program
**/
}

/*

gcc -Wall -I$HOME/local/include MyProg.c -L$HOME/local/lib -lcunit -o myprog
*/
