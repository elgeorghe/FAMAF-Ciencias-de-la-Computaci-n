#include "types.h"
#include "param.h"
#include "memlayout.h"
#include "riscv.h"
#include "defs.h"
#include "sem.h"
#include "proc.h"

struct {
    struct spinlock lock;
    struct semaforo sems[NSEM];
}semtable;

//Inicializa tabla de semaforos
void seminitsys(void){
    initlock(&semtable.lock, "semtable");
    for(int i = 0; i < NSEM; i++){
        semtable.sems[i].in_use = 0;
        initlock(&semtable.sems[i].lock, "semaforo");
    }
}

//Busca semaforo por nombre, devuelve indice o -1 si no lo encuentra
int find_sem(int name){
    for(int i = 0; i < NSEM; i++){
        if(semtable.sems[i].in_use && semtable.sems[i].name == name){
            return i;
        }
    }
    return -1;
}

//Busca semaforo vacio en la lista, devuelve indice o -1 si no lo encuentra
int find_free_sem(void){
    for(int i = 0; i < NSEM; i++){
        if(!semtable.sems[i].in_use){
            return i;
        }
    }
    return -1;
}

//Syscall sem_open: Crea un semaforo en la lista, devuelve indice o 0 si no puede crear
uint64 sem_open(int sem, int value) {
  
    //Acquire lock de la tabla
    acquire(&semtable.lock);

    //Checkear si el semaforo existe
    int indx = find_sem(sem);
    if(indx >= 0){
        release(&semtable.lock);
        return 0;
    }

    //Generar semaforo nuevo
    indx = find_free_sem();
    if(indx < 0){
        release(&semtable.lock);
        return 0;
    }

    semtable.sems[indx].name = sem;
    semtable.sems[indx].value = value;
    semtable.sems[indx].in_use = 1;

    release(&semtable.lock);


    
    return indx+1;
}

//Syscall sem_close: Libera un semaforo en la lista, devuelve 1 si no hay errores, devuelve 0 si hay algun error 
uint64 sem_close(int sem){
    
    acquire(&semtable.lock);

    int index = find_sem(sem);
    //me aseguro que el semaforo existe
    if (index==-1){
        release(&semtable.lock);
        return 0;
    }
    
    //Semaforo fuera de uso
    if(semtable.sems[index].in_use == 0){
        release(&semtable.lock);
        return 0;
    }

    semtable.sems[index].in_use = 0;

    release(&semtable.lock);
    return 1;
}

//Syscall sem_up: Incrementa un semaforo, devuelve 1 si no hay errores, devuelve 0 si hay error
uint64 sem_up(int sem){
    

    int index = find_sem(sem);
    //me aseguro que el semaforo existe
    if (index==-1){
        return 0;
    }

    //Acquire lock de este semaforo
    acquire(&semtable.sems[index].lock);

    if(semtable.sems[index].value<1){
        semtable.sems[index].value ++;
    }
    

    //Wakeup al proceso esperando este semaforo
    wakeup(&semtable.sems[index].value);

    release(&semtable.sems[index].lock);
    return 1;
}

//Syscall sem_down: Decrementa un semaforo, devuelve 1 si no hay errores, devuelve 0 si hay error
uint64 sem_down(int sem){
    
    int index = find_sem(sem);
    //me aseguro que el semaforo existe
    if (index==-1){
        return 0;
    }

    //Acquire lock de este semaforo
    acquire(&semtable.sems[index].lock);
    
    

    //Bloquear wakeup   
    while(semtable.sems[index].value == 0){
        sleep(&semtable.sems[index].value, &semtable.sems[index].lock);
    }
    //Decrementar value
    if(semtable.sems[index].value >0){
        semtable.sems[index].value--;
    }
    

    release(&semtable.sems[index].lock);
    return 1;
}