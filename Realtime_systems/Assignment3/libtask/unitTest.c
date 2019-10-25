#include <stdio.h>
#include <stdlib.h>
#include <CUnit/Basic.h>
//Change this if you want another limit :)
int up2number = 1000;


/**
In order to run the files, check that working_primes is an executable using chmod.

**/
void compare_primes(){
  FILE *expected;
  FILE *input;
  int CHAR_MAX_LEN = 100;
  char data1[CHAR_MAX_LEN];
  char data2[CHAR_MAX_LEN];

  char c[20];
  //CHANGE TO WORKING_PRIMES :)
  sprintf(c, "./working_primes %d", up2number);
  expected = popen(c, "r");

  sprintf(c, "./primes %d", up2number);
  input = popen(c, "r");

  CU_ASSERT(NULL != expected);
  CU_ASSERT(NULL != input);

  while (fgets(data1, CHAR_MAX_LEN, expected) != NULL){
    if (fgets(data2, CHAR_MAX_LEN, input) != NULL){
      //printf("%s - %s", data1, data2);
      CU_ASSERT(strcmp(data1, data2) == 0);
    }
  }
}


int main(int argc, char **argv){
  if (argc > 1)
      up2number = atoi(argv[1]);

	CU_pSuite pSuite = NULL;
	if (CUE_SUCCESS != CU_initialize_registry())
		return CU_get_error();

	pSuite = CU_add_suite("compare_primes",0,0);
	if (NULL == pSuite) {
      return CU_get_error();
  }
	if(NULL == CU_add_test(pSuite, "Compare primes",compare_primes)){
		CU_cleanup_registry();
  	return CU_get_error();
	}

	CU_basic_set_mode(CU_BRM_VERBOSE);
	CU_basic_run_tests();
	CU_cleanup_registry();
	return CU_get_error();
}
