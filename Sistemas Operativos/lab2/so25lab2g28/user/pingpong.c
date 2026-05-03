#include "../kernel/types.h"   
#include "../kernel/stat.h"
#include "user.h"

int ping_sem=0, pong_sem=1;

void ping ( int rondas){
    for(int i=0;i<rondas;i++){   
    sem_down(ping_sem);    
    write(1, "ping\n", 5);
    //sleep(2); 
    sem_up(pong_sem);
    
    }
    
}

void pong ( int rondas){
    for(int i=0;i<rondas;i++){
    sem_down(pong_sem);      
    write(1, "\tpong\n", 6);    
    //sleep(2);
    //if(0!=sem_up(pong_sem+1));
    //else if (sem_up(0)!=0);
    //else{
    sem_up(ping_sem); 
        //}

           
    }
    }


int main(int argc, char *argv[]){
    
    int pid;
    int rondas;

    if(argc != 2){
        printf("ERROR: Se debe introducir el numero de rondas--\n");
        exit(0);
    }

    rondas = atoi(argv[1]);

    if(rondas <= 0){
        printf("ERROR: El numero de rondas debe ser un numero natural--\n");
        exit(0);
    }
    //if(sem_open(ping_sem, 1)==0){
       while (sem_open(ping_sem, 1)==0 && ping_sem<32){
        ping_sem=ping_sem+2;
        pong_sem=pong_sem+2;
    } 
    //}

    
    sem_open(pong_sem, 0);   
    
    pid=fork();
    if(pid==0){
            pong(rondas);
           // exit(0);
    }
    else{
            ping(rondas);
            wait(0);
    }
    
    sem_close(ping_sem);
    sem_close(pong_sem);

    exit(0);
}

