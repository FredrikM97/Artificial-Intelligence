//  Created by Mohammadreza Mousavi [mohmou] on 9/5/14.
//  Updated by Masoumeh Taromirad on 11/08/16.
//  Updated by Wagner Morais and Johannes van Esch on 28/08/18.
//  Copyright (c) 2014 by Mohammadreza Mousavi [mohmou]. All rights reserved.

#ifndef lab0_iregister_h
#define lab0_iregister_h

/**
 *  iRegister
 *  An iRegister is a structure which represents an 32-bit register and
 *  is equipped with standard operations to modify and display them.
 */ 
typedef struct{
    int content;
} iRegister;

/**
 *  Bellow you find the declarations for the functions to modify and display the
 *  memory content of a iRegister data structure. Before each declaration, a brief 
 *  description about what the function shall do is given. 
 *  Later in this file, the documentation for the resetBit function is given. 
 *  Students should follow that format.
 */ 

/** 
 @brief Description: resets all the bits of the iRegister (to 0)
 @return void
 @param r is a pointer to a memory location of a iRegister data structure
 @pre iRegister != Null
 @post After resetAll(r) the iRegister is set to 0
 
 Properties:  
The selected register should be zero after resetAll()

 test-cases: 
 1) Allocate zeroes to iRegister r and e and try to reset and compare
 2) Allocate ones to iRegister r and try to reset and compare
 3,4) Allocate random values to iRegister r and try to reset -> repeat 32 times
 
 **/
void resetAll(iRegister *);
/** 
 @brief sets the i'th bit of the iRegister (to 1)
 @return void
 @param r is a pointer to a memory location of a iRegister data structure
 @param i Is i'th bit of the iRegister to be reset
 @pre 0 <= i < 32 and iRegister != Null
 @post After setBit(i,r) the i'th bit of iRegister is set to 1
 
 Properties:
 Must be within register limit 0 <= i < 32
 
 test-cases: 
1) Set r to 0 and e to 1. SetBit(0,&r) and compare
2) Set r to 1 and e to 0x80000001. SetBit(31,&r) and compare
3,4) Set r and e to zero try to set a bit out of bounds (over and under limits)
5) Loop and set random bit in r, compare with e if equal value is stored 
**/
void setBit(int, iRegister *);

/** 
 @brief sets all the bits of the iRegister (to 1)
 @return void
 @param r is a pointer to a memory location of a iRegister data structure
 @pre iRegister != Null
 @post After setAll(r) all bits in iRegister is set to 1
 
 Properties:
 All inside of register must be 1
 
 test-cases: 
1,2,3,4) Set e to -1
1) Use setAll(&r) and compare 
2) Set r to -1 use setAll(&r) and compare
3,4) Loop and set r to random value, set all compare to e 

**/
void setAll(iRegister *);

/** 
 @brief returns the i'th bit of the iRegister as an integer (1 if it is set, or 0 otherwise)
 @return bit in i'th position 
 @param r is a pointer to a memory location of a iRegister data structure
 @param i Is i'th bit of the iRegister 
 @pre 0 <= i < 32 and iRegister != Null
 @post After getBit(i,r) return i'th bit in iRegister
 
 Properties:
  Must be within register limit 0 <= i < 32
 
 test-cases: 
1,2,3,4) Set bit to 56, Set r to 0xE0000007
1) getBit(0,&r) and compare not equal
2) getBit(0,&r) and compare equal
3) getBit(31,&r) and compare equal
4) getBit(-1,&r) and check if it returns -1 (when out of bounds)
**/
int getBit(int, iRegister *);

/** 
 @brief set the first pos and the second a value of four bits of the nipple to the iRegsiter
 @param r is a pointer to a memory location of a iRegister data structure
 @param i Is i'th Nibble of the iRegister
 @param val Is value to be set in register
 @pre 0 <= i < 32 and 0 <= val <= 15 and iRegister != Null 
 @post After assignNibble(i,i,r) change the value of i'th position in the Nibble to val
 
 Properties:
  Must be within register limit 0 <= i < 32
 test-cases: 
1,2,3) Set e with three active nibbles and r as 0, assignNibble with different values and compare
4) If changing nibble try to overwrite previous one
5,6,7,8) Test out of bounds 

**/
void assignNibble(int, int, iRegister *);

/** 
 @brief Get the first (for pos=1) or the second (for pos=2) four bits of iRegsiter
 @return Nibble in i'th position 
 @param r is a pointer to a memory location of a iRegister data structure
 @param i Is i'th bit of the iRegister
 @pre 0 <= i < 32 and iRegister != Null
 @post After getNibble(i,r) get the value between 0-15 in the i'th position
 
 Properties:
  Must be within register limit 0 <= i < 32
 test-cases: 
1,2) Set e to 0, r to 1793,
1) compare not equal to getNibble(1,&r) equal e
2) compare getNibble(2,&r) equal e
3) Set e to 7,r to 1793, compare getNibble(3,&r) equal 7
4,5) Check out of bounds
**/
int getNibble(int, iRegister *);

/** 
 @brief returns a pointer1 to an array of 32 characters, with each character 
 *  representing the corresponding bit of the iRegister, i.e., if the bit is set,
 *  then the character is "1" (ASCII char with code 49), or otherwise is "0" 
 *  (ASCII char with code 48)
 @param r is a pointer to a memory location of a iRegister data structure
 @return all bits in regisiter as a char
 @pre iRegister != Null
 @post return 32 bit character containing the bit values of iRegister
 
 Properties:
 Return a char of 32 bits
 test-cases: 
1,2,3,4) Set r different values, memcmp with manual bit (string) and check if equal

**/
char *reg2str(iRegister);

/** 
 @brief shifts all the bits of the iRegister to the right by n palces (appends 0 
 *  from the left)
 @param r is a pointer to a memory location of a iRegister data structure
 @param i Is i'th bit of the iRegister
 @pre 0 <= i < 32 and iRegister != Null
 @post After shiftRight(int, iRegister *) shift iRegister i'th bits to the right
 
 Properties:
  Must be within register limit 0 <= i < 32
 test-cases: 
1,2,3) Set e, set r, shiftRight(x,&r), were x is depending on how many shifts needed to get same output
4,5) Check ot of bounds, over and under
**/
void shiftRight(int, iRegister *);

/** 
 @brief shifts all the bits of the iRegister to the left by n palces (appends 0 
 *  from the right)
 @param r is a pointer to a memory location of a iRegister data structure
 @param i Is i'th bit of the iRegister
 @pre 0 <= i < 32 and iRegister != Null
 @post After shiftLeft(int, iRegister *) shift iRegister i'th bits to the left
 
 Properties:
  Must be within register limit 0 <= i < 32

 
 test-cases: 
1,2,3) Set e, set r, shiftleft(x,&r), were x is depending on how many shifts needed to get same output
4,5) Check ot of bounds, over and under
**/
void shiftLeft(int, iRegister *);

/** 
@brief Resets the i'th bit of the iRegister (to 0)

@param i Is i'th bit of the iRegister to be reset
@param r A pointer to a memory location of a iRegister data structure.
@return void
@pre 0 <= i < 32 and iRegister != Nul
@post after reset(i, r) the i'th bit of iRegister is 0, all other 
bits remain unchanged
properties: 
Must be within register limit 0 <= i < 32

test-cases: 
1,2) Set r, resetBit(0,&r) compare if equal
3) check out of bounds (over and under)
4) Loop and check random values after resetting one bit.
 */
void resetBit(int, iRegister *);

#endif
