//  Created by Mohammadreza Mousavi [mohmou] on 9/5/14.
//  Updated by Masoumeh Taromirad on 11/08/16.
//  Updated by Wagner Morais and Johannes van Esch on 28/08/18.
//  Copyright (c) 2014 by Mohammadreza Mousavi [mohmou]. All rights reserved.

#include <stdlib.h>
#include <stdio.h>
#include "iregister.h"
#include <cstring>
#include <assert.h>
#include <time.h>
#include <limits.h>


void Tests();
void Test_setAll();
void Test_setBit();
void Test_resetAll();
void Test_reg2str();
void Test_resetBit();
void Test_getNibble();
void Test_shiftRight();
void Test_shiftLeft();
void Test_getBit();
void Test_assignNibble();






int main (){	
	/* Put all your test cases for the implemented functions here */
	Tests();
	return 0;
}

void Tests(){
	printf("Start tests \n\n");
	
	Test_resetAll();
	Test_setBit();
	Test_setAll();
	Test_getBit();
	Test_assignNibble();	
	Test_getNibble();
	Test_reg2str();
	Test_shiftRight();
	Test_shiftLeft();
	Test_resetBit();
	
	printf("\nall tests have been comlpeted\n");
}

void Test_resetAll(){
	iRegister r;
	iRegister e;
	srand(time(0));
	int x;
	e = {0}; //set all bits in the control
	
	r = {0};
	resetAll(&r);
	assert(e.content == r.content); //test if all bits get set if r is only zeros
	
	r = {-1};
	resetAll(&r);
	assert(e.content == r.content); //tests if all bits remaining on if r starts white all bits set
	
	for(x = 0; x < 32;x++){ //test resetAll on random int nummbers
		r = {rand()+1}; 		// set random positive int
		resetAll(&r);
		assert(e.content == r.content);
	}
	
	printf("resetAll works\n" );
}

void Test_setBit(){ 
	iRegister r;
	iRegister e;
	srand(time(0));
	int x, temp;
	e = {1};//set all bits in control

	r = {0};		
	setBit(0,&r);
	assert(e.content == r.content); //test setting the first bit
	
	e = {-2147483647};
	setBit(31,&r);
	assert(e.content == r.content); //test setting the last bit and that it retain the previous changes

	r = {0};
	e = {0};
	setBit(-1,&r);
	assert(e.content == r.content); //test that going below the register doesnt break any thing
	
	setBit(32,&r);
	assert(e.content == r.content);//testing in setting a bit over the register that it dosent break anything

	r = {0};
	e = {0};
	for(x = 0; x < 35;x++){ //test setBit on random int number position and set bit on a already set bit
		temp = rand()%31;
		setBit(temp,&r);
		e = {e.content | 1<<temp};
		assert(e.content == r.content);
	}
	
	
	printf("setBit works\n" );
}

void Test_setAll(){
	iRegister r;
	iRegister e;
	srand(time(0));
	int x;
	e = {-1}; // set all bits in control
	
	r = {0};
	setAll(&r);
	assert(e.content == r.content);//test if all bits get set if r is only zeros
	
	r = {-1};
	setAll(&r);
	assert(e.content == r.content);//tests if all bits remaining on if r starts white all bits set
	
	for(x = 0; x < 32;x++){ //test setall on random int nummbers
		r = {rand()}; 		// set random positive int
		setAll(&r);
		assert(e.content == r.content);
	}
	
	printf("setAll works\n" );
}

void Test_getBit(){ 
	iRegister r;
	iRegister e;
	int x,y;
	srand(time(0));
	e = {56};//set all bits in control

	r = {-536870905};	
	
	assert(0 != getBit(0,&r)); //test first bit
	assert(1 == getBit(0,&r));
	
	assert(1 == getBit(31,&r)); // test last bit
	
	assert(-1 == getBit(-1,&r));//test out of bounce
	assert(-1 == getBit(32,&r));//test out of bounce
	/* 
	for(x = 0; x < 32;x++){ //test that it only returns 0 or 1
		r = {rand()}; // set random positev int
		for(y = 0; y < 32;y++){ 
			assert(1 == getBit(y,&r) || 0 == getBit(y,&r));
		}
	}
	*/
	printf("getBit works\n" );
}

void Test_assignNibble(){
	iRegister r;
	iRegister e;
	
	r = {0};
	e ={-2147483593};
	
	int x;
	
	assignNibble(1,7,&r); //test that it can set specific nibbels
	assert(e.content != r.content); 
	assignNibble(2,3,&r);
	assert(e.content != r.content); 
	assignNibble(8,8,&r);
	assert(e.content == r.content); 
	
	assignNibble(8,0,&r); //see if assignNibble replaces all bits in the nibble
	assert(0 < r.content); 
	

	r = {0};
	e ={0};
	
	assignNibble(0,4,&r);
	assert(e.content == r.content); //test out of bounce
	
	assignNibble(9,4,&r);
	assert(e.content == r.content); //test out of bounce
	
	assignNibble(1,-1,&r);
	assert(e.content == r.content); //test out of bounce
	
	assignNibble(-1,16,&r);
	assert(e.content == r.content); //test out of bounce
	
	
	printf("assignNibble works\n" );
}

void Test_getNibble(){ 
	iRegister r;
	iRegister e;
	e = {0};//set all bits in control

	r = {1793};	
	assert(e.content != getNibble(1,&r));//test if it kan get info in a given nibble

	assert(e.content == getNibble(2,&r));//test if it kan get info in a given nibble
	
    e = {7};
	assert(7 == getNibble(3,&r)); //test if it kan get info in a nibble
	
	assert(-1 == getNibble(-1,&r)); //test out of bounce
	
	assert(-1 == getNibble(9,&r)); //test out of bounce
	
	
	printf("getNibble works\n" );
}

void Test_reg2str(){
	iRegister r;

	r = {0};	
	assert(memcmp("00000000000000000000000000000000", reg2str(r),32) == 0); //test that r and the bit info is the same
	
	assert(memcmp("00000000000000000000000000000001", reg2str(r),32) != 0);//test that reg2str only works agenst a given r
	
	r = {-1};
	assert(memcmp("11111111111111111111111111111111", reg2str(r),32) == 0);//test that r and the bit info is the same
	
	r = {1431655765};
	assert(memcmp("01010101010101010101010101010101", reg2str(r),32) == 0);//test that r and the bit info is the same
	
	r = {123456789};
	assert(memcmp("00000111010110111100110100010101 ", reg2str(r),32) == 0);//test that r and the bit info is the same
	
	printf("reg2str works\n" );
}

void Test_shiftRight(){
	iRegister r;
	iRegister e;
	e = {33554432};//set all bits in control

	r = {-2147483587};	
	shiftRight(6,&r);
	assert(e.content == r.content); //test r by shifting right write a negative nummber
	
	e = {0};
	r = {-1};	
	shiftRight(32,&r);
	assert(e.content == r.content); //test to shift the full register
	
	shiftRight(32,&r);
	assert(e.content == r.content); //test to shift the full register write only 0s
	
	e = {-1};
	r = {-1};	
	shiftRight(0,&r);
	assert(-1 == r.content); //test out of bounce
	
	shiftRight(33,&r);
	assert(-1 == r.content); //test out of bounce
	
	printf("shiftRight works\n" );
}

void Test_shiftLeft(){ 
	iRegister r;
	iRegister e;
	e = {56};//set all bits in control

	r = {-536870905};	
	shiftLeft(3,&r);
	assert(e.content == r.content); //test r by shifting right write a negative nummber
	
	e = {0};
	r = {-1};	
	shiftLeft(32,&r);
	assert(e.content == r.content); //test to shift the full register
	
	shiftLeft(32,&r);
	assert(e.content == r.content); //test to shift the full register write only 0s
	
	e = {-1};
	r = {-1};	
	shiftLeft(0,&r);
	assert(-1 == r.content); //test out of bounce
	
	shiftLeft(33,&r);
	assert(-1 == r.content); //test out of bounce
	
	printf("shiftLeft works\n" );
}

void Test_resetBit(){
	iRegister r;
	iRegister e;
	int x,temp;
	srand(time(0));
	e = {0};//set all bits in control

	r = {1};	
	resetBit(0,&r);
	assert(e.content == r.content); //test setting the first bit
	
	r = {-2147483647};
	resetBit(31,&r);
	resetBit(0,&r);
	assert(e.content == r.content); //test setting the last bit and that it retains the previous register
	
	resetBit(-1,&r);
	assert(e.content == r.content); //test that going below the register bounce 
	
	resetBit(32,&r);
	assert(e.content == r.content);//testing in setting a bit over the register bounce 
	
	r = {-1};
	e = {-1};
	for(x = 0; x < 35;x++){ //test resetBit on random int number position and reset a bit on a already been reset bit
		temp = rand()%31;
		resetBit(temp,&r);
		e = {e.content & ~(1<<temp)};
		//printf("temp = %d, \nr= %d,\ne = %d\n",temp, r.content, e.content);
		assert(e.content == r.content);
	}
	
	printf("resetBit works\n" );
}
