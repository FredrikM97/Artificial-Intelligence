#include "stdlib.h"
#include "stdio.h"
#include "math.h"
#include "TaylorSeries.h"


ExpStruct * iexp ( int x){
	ExpStruct *output = (ExpStruct*) malloc(sizeof (ExpStruct)); //declare structure and allocate it to memory

	float i; //init values
	int n = abs(x)+1;
	float sum = 1;
	float fac = 1;

	for(i = 1; i < n; i++){ //doing the Taylor Series one step at the time
		fac *= i;
		sum += (float)pow(x,i)/fac;
	}

	output->expInt = (int)sum;//allocate the values to the structure
	output->expFraction = (int)((sum - (long)sum)*100.0);

	return output;//return the struktur
}
