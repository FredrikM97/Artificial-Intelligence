#include <stdlib.h>
#include <stdio.h>
//#include <math.h>
#include "TaylorSeries.h"


ExpStruct * iexp ( int x){
	ExpStruct *output = (ExpStruct*) malloc(sizeof (ExpStruct)); //declare structure and allocate it to memory

	float i; //init values
	int n = abs(x)+1;
	float sum = 1;
	float fac = 1;

	for(i = 1; i < n; i++){ //doing the Taylor Series one step at the time
		fac *= i;
		sum += (float)data2pow(x,i)/fac;
	}

	output->expInt = (int)sum;//allocate the values to the structure
	output->expFraction = (float)((sum - (int)sum)*100);

	return output;//return the struktur
}
float data2pow(int x,int n){
		float val = 1;
    int i;

    for (i = 0; i < n; ++i){
        val *= x;
		}
    return(val);
}
