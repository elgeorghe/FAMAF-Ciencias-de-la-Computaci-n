#ifndef _FUNCIONES_EXTRAS_H_
#define _FUNCIONES_EXTRAS_H_

// Returns the filepath of the archive after compile
char *parse_filepath (int argc , char *argv[]);

// Returns the number of elements in the archive. It also separates the indexes and letters in separate arrays.
unsigned int data_from_file(const char *path, unsigned int indexes[], char letters[], unsigned int max_size);

// Fills sorted with the chars in letters in their right index found in indexes
void sort(char sorted[] , unsigned int indexes[] , char letters[] , unsigned int length);

#endif