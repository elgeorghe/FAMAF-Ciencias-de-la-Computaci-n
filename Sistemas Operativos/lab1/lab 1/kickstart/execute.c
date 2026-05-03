/* Ejecuta comandos simples y pipelines.
 * No toca ningún comando interno.
 */



#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <glib.h>
#include <assert.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>   
#include <check.h>
#include <signal.h>


#include "tests/syscall_mock.h"
#include "execute.h"
#include "command.h"
#include "builtin.h"


void execute_pipeline(pipeline apipe){
    
    scommand cmd = NULL;
    bool foreground=pipeline_get_wait(apipe);
    int length = pipeline_length(apipe);
    int *pipes = NULL;
    pipes = malloc (2* (length-1) * sizeof(int));
    for (int i = 0; i < length-1; i++) 
    {
        pipe(pipes + i*2);
    }
    pid_t *pid = malloc(sizeof(int)*length);
    for(int i=0; i<length; i++)
    {   
        cmd =NULL;
        cmd =pipeline_front(apipe);
        int in=0, out=1;
        char * red_in=scommand_get_redir_in(cmd),* red_out=scommand_get_redir_out(cmd);

       

        if(builtin_is_internal(cmd))
        {
            char * com=NULL;
            com=scommand_front(cmd); 


            if((strcmp(com,"help") == 0))
                {   
                    pid [i]=fork();
                    if(pid[i]==0)
                    {
                        if(red_out != NULL) 
                        {
                            out=open(red_out,O_CREAT | O_WRONLY , 0644);
                        }

                        if(red_out!=NULL)
                        {
                            dup2(out,STDOUT_FILENO);
                            close(out);
                        }
                        else if(((length-1) !=i))
                        {
                            dup2(pipes[i*2+1],STDOUT_FILENO);
                        } 

                        for (int j = 0; j < 2*(length-1); j++) 
                        {
                            close(pipes[j]);
                        }
                        
                        builtin_run(cmd);  
                        exit(0);
                    }
                    
                }
            else if((builtin_alone(apipe)))
            {
           
                   builtin_run(cmd);  
                
            }
        }
        
        else 
        {
            unsigned int cmd_length = scommand_length(cmd);

           pid [i]=fork();
            if(pid[i] == 0)
            {
                char **argv = malloc((cmd_length +1) * sizeof(char));
                for(unsigned int e=0;e<cmd_length;e++)
                {
                    argv[e]=strdup(scommand_front(cmd));
                    scommand_pop_front(cmd);
                }
                argv[cmd_length] = NULL;
                 
                if(red_in != NULL)
                {
                    in=open(red_in,O_RDONLY, 0644);
                }
                if(red_out != NULL) 
                {
                    out=open(red_out,O_CREAT | O_WRONLY , 0644);
                }

                if(red_in!=NULL)
                {
                    dup2(in,STDIN_FILENO);
                    close(in);
                }

                else if(i>0 )
                {
                    dup2(pipes[(i-1)*2],STDIN_FILENO);
                }

                if(red_out!=NULL)
                {
                    dup2(out,STDOUT_FILENO);
                    close(out);
                }
                else if((length-1) > i )
                {
                    dup2(pipes[i*2 + 1],STDOUT_FILENO);
                }   
                

                for (int j = 0; j < 2*(length-1); j++) 
                {
                close(pipes[j]);
                }

                execvp(argv[0], argv);
                perror("execvp");
                exit(1);
                free(argv);
                argv = NULL;
            }
            
            
        }
        pipeline_pop_front(apipe);
    }
    for (int i = 0; i < 2*(length-1); i++) 
                {
                    close(pipes[i]);
                }
    if (foreground)
    {
        for(int j=0; j<length;j++)
        {
            waitpid(pid[j], NULL, 0);
        }
    }
    else 
    {
        
    }
    free(pipes);
    pipes = NULL;
    free(pid);
    pid = NULL;
}






/*
 * Ejecuta un pipeline, identificando comandos internos, forkeando, y
 *   redirigiendo la entrada y salida. puede modificar `apipe' en el proceso
 *   de ejecución.
 *   apipe: pipeline a ejecutar
 * Requires: apipe!=NULL
 */

