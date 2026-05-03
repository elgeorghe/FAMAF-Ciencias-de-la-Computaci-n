#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <glib.h>
#include <assert.h>
#include <unistd.h>
#include <fcntl.h>

#include <check.h>
#include <signal.h>

#include "tests/syscall_mock.h"
#include "command.h"
#include "builtin.h"

bool builtin_is_internal(scommand cmd)
{
    assert(cmd != NULL); // requires

    char *name = scommand_front(cmd);

    return (strcmp(name, "cd") == 0 || strcmp(name, "help") == 0 || strcmp(name, "exit") == 0);
}

bool builtin_alone(pipeline p)
{
    assert(p != NULL); //requires

    bool res = true;

    res = (pipeline_length(p) == 1) && builtin_is_internal(pipeline_front(p));

    assert((res == (pipeline_length(p) == 1)) && builtin_is_internal(pipeline_front(p))); //ensures

    return res;
}

void builtin_run(scommand cmd)
{
    assert(builtin_is_internal(cmd));
    char *command = scommand_front(cmd);
    if (strcmp(command, "exit") == 0)
    {
        
        exit(EXIT_SUCCESS);
    }
    else if (strcmp(command, "help") == 0)
    {
            printf("Nombre del shell: MyBash\n"
                "Autores: man SistOp\n"
                "cd: cambia  el directorio de trabajo\n"
                "help: lista de comandos y breve descripcion de cada uno\n"
                "exit: termina shell de manera limpia liberando recursos\n");
        
       
    }
    else if (strcmp(command, "cd") == 0)
    {
        scommand_pop_front(cmd);
        char * path =NULL;
        path = strdup(scommand_to_string(cmd));
        
        if (path!=NULL)
        {
            chdir(path);
        }
        
        free (path);
    }
    else
    {
        perror("no es un comando interno");
        exit(1);
    }
    free(command);
}