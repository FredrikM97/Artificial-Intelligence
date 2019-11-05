/*
    Part of the Real-Time Embedded Systems course at Halmstad University
    Copyright (c) 2017, Sebastian Kunze <sebastian.kunze@hh.se>
    All rights reserved.
*/

#include <stdio.h>
#include <stdlib.h>
#include <rpi3.h>
#include "TaylorSeries.h"
#include "piface.h"
#include "iregister.h"
#include <time.h>

void display_Controller(int, int *);
extern void led_Controller();

int LAMP_STATUS = 0; //Status of lamp
int main(){
    int CircleStuff = 0; //Global interleaving checkthingy
    iRegister lamp = {1};
    shiftLeft(18,&lamp);
    /* Enable GPIO16 as an output */
    GPIO->GPFSEL1 |= lamp.content;
  
    /* Write to PiFace's LCD screen */
    piface_puts("Hello World!\n");
    int i=0;
    //int x = 0;
    while (1){
      display_Controller(i, &CircleStuff); //Takes to long time, split it up even more and call on led_Controller
      i++;
    }
	return 0;
}

void display_Controller(int i, int *CircleStuff){
  char data[32];
  ExpStruct *temp=iexp(i, CircleStuff);
  sprintf(data, "%d: %d.%d",i,temp->expInt,temp->expFraction);
  piface_puts(data);
  piface_delay();
  piface_clear();
  free(temp);
}
void led_Controller(){
  iRegister lamp = {1};
  shiftLeft(16,&lamp);
  /* Iteratively turn on and off the LED */
  LAMP_STATUS = !LAMP_STATUS;
  if(LAMP_STATUS){
    GPIO->GPCLR0 |= lamp.content;
  }else{
    GPIO->GPSET0 |= lamp.content;
  }
}
