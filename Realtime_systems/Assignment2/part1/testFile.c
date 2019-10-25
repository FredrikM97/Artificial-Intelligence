void test_expFraction(void){
	srand(time(0));
	int i, test;

	for(i = 0; i < 100;i++){//testar så att det inte kan bli störe en 2 desimaler
		test = iexp(rand()%22)->expFraction;
		CU_ASSERT(100 > test && test >= 0);
	}
}


void test_BREAKiexp(void){ //try to break iexp
	srand(time(0));
	int i;
	expStruct test;

	test = iexp(-21); //test min int
	CU_ASSERT(test != NULL);
	free(test);

	test = iexp(0);
	CU_ASSERT(test != NULL); //test 0
	free(test);

	test = iexp(22);//test max int
	CU_ASSERT(test != NULL);
	free(test);

	for(i = 0; i < 1000;i++){ //test random int
		test = iexp(rand()%22);
		CU_ASSERT(test != NULL);
		free(test);
	}
}


void test_iexp(void){ //try to break iexp
	srand(time(0));
	int i;
	expStruct test;

	test = iexp(0);
	CU_ASSERT(test->expInt ==  1);
	CU_ASSERT(test->expFraction ==  0);
	CU_ASSERT(test->expInt ==  1 && test->expFraction ==  0);
	free(test);

	test = iexp(4);
	CU_ASSERT(test-> expInt ==  34);
	CU_ASSERT(test-> expFraction ==  33);
	CU_ASSERT(test-> expInt ==  34 && test-> expFraction ==  33);
	free(test);

	test = iexp(10);
	CU_ASSERT(test-> expInt ==  12842);
	CU_ASSERT(test-> expFraction ==  30);
	CU_ASSERT(test-> expInt ==  12842 && test-> expFraction ==  30);
	free(test);

	test = iexp(-5);
	CU_ASSERT(test-> expInt ==  -12);
	CU_ASSERT(test-> expFraction ==  33);
	CU_ASSERT(test-> expInt ==  -12 && test-> expFraction ==  33);
	free(test);
}

//22
CU_ASSERT(test-> expInt ==  1994556672);
CU_ASSERT(test-> expFraction ==  0);
free(test);

//-22
CU_ASSERT(test-> expInt ==  150135344);
CU_ASSERT(test-> expFraction ==  0);
free(test);
