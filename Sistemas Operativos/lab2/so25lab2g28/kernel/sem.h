#include "spinlock.h"

#define NSEM 32
#define SEM_NAME_LEN 32

struct semaforo{
    int name;
    int value;
    int in_use;
    struct spinlock lock;
};

void seminitsys ();
