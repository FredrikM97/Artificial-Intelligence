#include <stdlib.h>
#include <stdio.h>
#include "TaylorSeries.h"

ExpStruct * iexp (int x, int *CircleStuff){
	ExpStruct *output = (ExpStruct*) malloc(sizeof (ExpStruct)); //declare structure and allocate it to memory
	float i; //init values
	int n = abs(x)+1;
	float sum = 1;
	float fac = 1;

	for(i = 1; i < n; i++){ //doing the Taylor Series one step at the time
		fac *= i;
		sum += (float)data2pow(x,i, CircleStuff)/fac;
	}

	output->expInt = (int)sum;//allocate the values to the structure
	output->expFraction = (float)((sum - (int)sum)*100);

	return output; //return the struktur
}
float data2pow(int x,int n, int *CircleStuff){
	float val = 1;
    int i;
	
	for (i = 0; i < n; ++i){
		val *= x;
		if(*CircleStuff % 200 == 0){
			led_Controller();
		}
		*CircleStuff++;
	}
	return(val);
}
