#include "../kernel/types.h"   
#include "../kernel/stat.h"
#include "user.h"

int ta_sem = 0, te_sem=1 , ti_sem=2;
int sem_bef=0;
void ta(int repeats){
    for(int i = 0; i < repeats; i++){
        sem_down(ta_sem);
        write(1, "TA", 3);
        //sleep(5);
        sem_up(te_sem);
    }
}

void te(int repeats){
    for(int i=0; i<repeats ; i++){
        sem_down(te_sem);
        write(1, "TE", 3);
        //sleep(5);
        sem_up(ti_sem);
    }
}

void ti(int repeats){
    for(int i=0 ; i<repeats; i++){
        sem_down(ti_sem);
        write(1, "TI\n", 4  );
        //sleep(5);
      //  if(0 != sem_up(0));
        //else{
            sem_up(ta_sem);
      //  }
        
    }
}

int main(int argc, char* argv[]){
    int pid1, pid2;
    int repeats;

    if(argc != 2){
        printf("--Se debe introducir el numero de repeticiones--\n");
        exit(0);
    }

    repeats = atoi(argv[1]);

    if(repeats <= 0){
        printf("--ERROR: El numero de repeticiones debe ser natural--\n");
        exit(0);
    }
    while (sem_open(ta_sem, 1)==0 && ta_sem<32){
        ta_sem=ta_sem+3;
        te_sem=te_sem+3;
        ti_sem=ti_sem+3;
    }
   // sem_open(ta_sem, 1);
    sem_open(te_sem, 0);
    sem_open(ti_sem, 0);

    pid1 = fork();

    if(pid1 == 0){
        pid2 = fork();
        if(pid2 == 0){
            ti(repeats);
            exit(0);
        }else{
            te(repeats);
            exit(0);
        }
        wait(0);
    }else{
        ta(repeats);
        wait(0);
    }
    sem_close(ta_sem);
    sem_close(te_sem);
    sem_close(ti_sem);
    
    exit(0);
}