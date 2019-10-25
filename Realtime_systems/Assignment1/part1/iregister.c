//  Created by Mohammadreza Mousavi [mohmou] on 9/5/14.
//  Updated by Masoumeh Taromirad on 11/08/16.
//  Updated by Wagner Morais and Johannes van Esch on 28/08/18.
//  Copyright (c) 2014 by Mohammadreza Mousavi [mohmou]. All rights reserved.
 
#include <stdlib.h>
#include <stdio.h>
#include "iregister.h"



void resetBit(int i, iRegister *r) {
	if(i <= 31 && i >= 0){
		r->content &= ~(1 << i);
	}else{
		//error protokol
	} 
}

void setBit(int i, iRegister *r) {
	if(i <= 31 && i >= 0){
		r->content |= (1 << i);
	}else{
		//error protokol
	}
}

void setAll(iRegister *r) {
	r->content = ~0;
}

void resetAll(iRegister *r) {
	r->content = 0;
}


int getBit(int i, iRegister *r){
	if(i <= 31 && i >= 0){
		return (r->content >> i) & 1;
	}else{
		//error protokol
		return -1;
	}
}

void assignNibble(int pos, int val, iRegister *r){	
	if(pos <= 8 && pos >= 1 && val <=15 && val >= 0){
		r->content &= ~(0xF<<((pos-1)*4)); //Masking
		r->content |= (val<<((pos-1)*4));
	}else{
		//error protokol
	}
}

int getNibble(int pos, iRegister *r){
	if(pos <= 8 && pos >= 1){
		return (r->content >> ((pos-1)*4) & 0xF);
	}
	//error protokol
	return -1;
}

char *reg2str(iRegister r) {
	static char output[33];
	
	int i; 
	for (i = 31; i >= 0; i--){
		if(getBit(i,&r) == 1) {
			output[31-i] = '1';
		}else {
			output[31-i] = '0';
		}
	}
	output[32] = 0x0;
	return output;
}

void shiftRight(int i, iRegister *r){
	if(i < 32 && i > 0){
		if(getBit(31,r) == 1){
			r->content = (r->content) >> 1;
			resetBit(31,r);
			r->content = (r->content) >> i-1;
		}else{
			r->content = (r->content) >> i;
		}
	}else{
		//error protokol
	}
}

void shiftLeft(int i, iRegister *r){
	if(i < 32 && i > 0){
		r->content = (r->content)<<i;
	}else{
		//error protokol
	}
}
