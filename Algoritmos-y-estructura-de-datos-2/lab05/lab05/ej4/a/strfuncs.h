/**
*  @file strfuncs.h
*/

#ifndef __STRFUNCS_H__
#define __STRFUNCS_H__

/**
* @brief Calculates the length of the string point with str
* @return Unsigned int
*/
size_t string_length(const char *str);

/**
* @brief Sets a new string on dynamic memory with the chars in str that are different to c
* @return Pointer
*/
char *string_filter(const char *str, char c);

#endif