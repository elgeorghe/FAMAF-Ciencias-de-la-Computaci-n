#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <glib.h>
#include <assert.h>

#include "command.h"


/* scommand: comando simple.
 * Ejemplo: ls -l ej1.c > out < in
 * Se presenta como una secuencia de cadenas donde la primera se denomina
 * comando y desde la segunda se denominan argumentos.
 * Almacena dos cadenas que representan los redirectores de entrada y salida.
 * Cualquiera de ellos puede estar NULL indicando que no hay redirección.
 *
 * En general, todas las operaciones hacen que el TAD adquiera propiedad de
 * los argumentos que le pasan. Es decir, el llamador queda desligado de la
 * memoria utilizada, y el TAD se encarga de liberarla.
 *
 * Externamente se presenta como una secuencia de strings donde:
 *           _________________________________
 *  front -> | cmd | arg1 | arg2 | ... | argn | <-back
 *           ---------------------------------
 *
 * La interfaz es esencialmente la de una cola. A eso se le
 * agrega dos accesores/modificadores para redirección de entrada y salida.
 */
    struct scommand_s {
        GList *command;
        char* out;
        char* in;
    };

typedef struct scommand_s * scommand;

scommand scommand_new(void){


    scommand new_command = malloc(sizeof(GList)* sizeof(char*));
    new_command->command =NULL;
    new_command->in =NULL;
    new_command->out =NULL;
    assert(new_command!=NULL && scommand_is_empty(new_command) && scommand_get_redir_in (new_command) == NULL && scommand_get_redir_out (new_command) == NULL);
    return new_command;
}
/*
 * Nuevo `scommand', sin comandos o argumentos y los redirectores vacíos
 *   Returns: nuevo comando simple sin ninguna cadena y redirectores vacíos.
 * Ensures: result != NULL && scommand_is_empty (result) &&
 *  scommand_get_redir_in (result) == NULL &&
 *  scommand_get_redir_out (result) == NULL
 */


scommand scommand_destroy(scommand self){
    
    assert(self!=NULL);
    if(self->command == NULL){
        if(self->in != NULL){
            free(self->in);
        }
        if(self->out != NULL){
            free(self->out);
        }
        free(self);
        self = NULL;
        assert(self==NULL);
        return self;
    }else{
        g_list_free_full(self->command, free);
        if(self->in != NULL){
            free(self->in);
        }
        if(self->out != NULL){
            free(self->out);
        }
        free(self);
        self=NULL;
        assert(self==NULL);
        return self;
    }
}
/*
 * Destruye `self'.
 *   self: comando simple a destruir.
 * Requires: self != NULL
 * Ensures: result == NULL
 */

/* Modificadores */

void scommand_destroy_void(scommand self){
    assert(self!=NULL);
    if(self->command == NULL){
        if(self->in != NULL){
            free(self->in);
        }
        if(self->out != NULL){
            free(self->out);
        }
        free(self);
        self = NULL;
        assert(self==NULL);
    }else{
        g_list_free_full(self->command, free);
        if(self->in != NULL){
            free(self->in);
        }
        if(self->out != NULL){
            free(self->out);
        }
        free(self);
        self=NULL;
        assert(self==NULL);
    }
}
/*
 * funcion destroy, pero devuelve void para poder usar en pipeline_destroy
 */

void scommand_push_back(scommand self, char * argument)
/*
 * Agrega por detrás una cadena a la secuencia de cadenas.
 *   self: comando simple al cual agregarle la cadena.
 *   argument: cadena a agregar. El TAD se apropia de la referencia.
 * Requires: self!=NULL && argument!=NULL
 * Ensures: !scommand_is_empty()
 */
{
    assert((self != NULL) && (argument != NULL));
    self->command = g_list_append(self->command, argument);
    assert(!scommand_is_empty(self));

}

void scommand_pop_front(scommand self)
/*
 * Quita la cadena de adelante de la secuencia de cadenas.
 *   self: comando simple al cual sacarle la cadena del frente.
 * Requires: self!=NULL && !scommand_is_empty(self)
 */
{ 
    assert((self != NULL) && (!scommand_is_empty(self)));
    self->command = g_list_remove(self->command,g_list_first(self->command)->data);
}

void scommand_set_redir_in(scommand self, char * filename){
    assert(self != NULL);
    self->in = filename;
}
void scommand_set_redir_out(scommand self, char * filename){
    assert(self != NULL);
    self->out = filename;
}
/*
 * Define la redirección de entrada (salida).
 *   self: comando simple al cual establecer la redirección de entrada (salida).
 *   filename: cadena con el nombre del archivo de la redirección
 *     o NULL si no se quiere redirección. El TAD se apropia de la referencia.
 * Requires: self!=NULL
 */

/* Proyectores */

bool scommand_is_empty(const scommand self){
    assert(self != NULL);
    return (self->command == NULL);
}
/*
 * Indica si la secuencia de cadenas tiene longitud 0.
 *   self: comando simple a decidir si está vacío.
 *   Returns: ¿Está vacío de cadenas el comando simple?
 * Requires: self!=NULL
 */

unsigned int scommand_length(const scommand self){
    assert(self != NULL);
    unsigned int result;
    if(self->command == NULL){
        result = 0;
    }else{
        result=g_list_length(self->command);
    }
    assert((result == 0) == scommand_is_empty(self));
    return result;
}
/*
 * Da la longitud de la secuencia cadenas que contiene el comando simple.
 *   self: comando simple a medir.
 *   Returns: largo del comando simple.
 * Requires: self!=NULL
 * Ensures: (scommand_length(self)==0) == scommand_is_empty()
 *
 */

char * scommand_front(const scommand self){
    assert((self != NULL)  &&  (!scommand_is_empty(self)));
    char *result = self->command->data;
    assert(result!=NULL);
    return result;
}
/*
 * Toma la cadena de adelante de la secuencia de cadenas.
 *   self: comando simple al cual tomarle la cadena del frente.
 *   Returns: cadena del frente. La cadena retornada sigue siendo propiedad
 *     del TAD, y debería considerarse inválida si luego se llaman a
 *     modificadores del TAD. Hacer una copia si se necesita una cadena propia.
 * Requires: self!=NULL && !scommand_is_empty(self)
 * Ensures: result!=NULL
 */

char * scommand_get_redir_in(const scommand self){
    assert(self != NULL);
    return self->in;

}
char * scommand_get_redir_out(const scommand self){
    assert(self != NULL);
    return self->out;
}
/*
 * Obtiene los nombres de archivos a donde redirigir la entrada (salida).
 *   self: comando simple a decidir si está vacío.
 *   Returns: nombre del archivo a donde redirigir la entrada (salida)
 *  o NULL si no está redirigida.
 * Requires: self!=NULL
 */

char * scommand_to_string(const scommand self){
    assert(self != NULL);

    //Caso comando vacio
    if(scommand_is_empty(self)){
        return g_strdup("");
    }

    GString *gstr_to_res = g_string_new(NULL);
    GList *current = self->command;
    bool first_arg = true;

    while(current != NULL){
        char *arg = (char *)current->data;
        

        //Espacio entre argumentos. Ignora el comando
        if(first_arg){
            first_arg = false;
        }else{
            g_string_append_c(gstr_to_res, ' ');
        }

        //Checkeo de comilla
        bool needs_quoting = false;
        for (char *p = arg; *p != '\0'; p++) {
            if (*p == ' ' || *p == '\t' || *p == '"' || *p == '\'' || 
                *p == '|' || *p == '>' || *p == '<' || *p == '&' || 
                *p == ';' || *p == '(' || *p == ')' || *p == '$' || 
                *p == '`' || *p == '\\' || *p == '*') {
                needs_quoting = true;
                break;
            }
        }


        //Añade argumentos con comilla si es necesario
        if (needs_quoting) {
            g_string_append_c(gstr_to_res, '\'');
            for (char *p = arg; *p != '\0'; p++) {
                if (*p == '\'') {
                    g_string_append(gstr_to_res, "'\\''");
                } else {
                    g_string_append_c(gstr_to_res, *p);
                }
            }
            g_string_append_c(gstr_to_res, '\'');
        } else {
            g_string_append(gstr_to_res, arg);
        }
        
        //Iteracion
        current = g_list_next(current);
    }


    //Añade redireccion de input
    if(self->in != NULL){
        g_string_append_printf(gstr_to_res, " < %s", self->in);
    }


    //Añade redireccion de output
    if(self->out != NULL){
        g_string_append_printf(gstr_to_res, " > %s", self->out);
    }
    
    //Convierte GString a C string(aka null terminated string)
    char *result = g_string_free(gstr_to_res, FALSE);                //g_string_free en FALSE asegura condicion del llamador
    assert(scommand_is_empty(self) || scommand_get_redir_in(self)==NULL || scommand_get_redir_out(self)==NULL || strlen(result)>0);
    return result;
}
/* Preety printer para hacer debugging/logging.
 * Genera una representación del comando simple en un string (aka "serializar")
 *   self: comando simple a convertir.
 *   Returns: un string con la representación del comando simple similar
 *     a lo que se escribe en un shell. El llamador es dueño del string
 *     resultante.
 * Requires: self!=NULL
 * Ensures: scommand_is_empty(self) ||
 *   scommand_get_redir_in(self)==NULL || scommand_get_redir_out(self)==NULL ||
 *   strlen(result)>0
 */


/*
 * pipeline: tubería de comandos.
 * Ejemplo: ls -l *.c > out < in  |  wc  |  grep -i glibc  &
 * Secuencia de comandos simples que se ejecutarán en un pipeline,
 *  más un booleano que indica si hay que esperar o continuar.
 *
 * Una vez que un comando entra en el pipeline, la memoria pasa a ser propiedad
 * del TAD. El llamador no debe intentar liberar la memoria de los comandos que
 * insertó, ni de los comandos devueltos por pipeline_front().
 * pipeline_to_string() pide memoria internamente y debe ser liberada
 * externamente.
 *
 * Externamente se presenta como una secuencia de comandos simples donde:
 *           ______________________________
 *  front -> | scmd1 | scmd2 | ... | scmdn | <-back
 *           ------------------------------
 */

 struct pipeline_s {
    GList *commands;
    bool background;
};
 
typedef struct pipeline_s * pipeline;

pipeline pipeline_new(void){

    pipeline new_pipeline = malloc(sizeof(GList)* sizeof(bool));
    new_pipeline->commands =NULL;
    new_pipeline->background =true; 
    assert(new_pipeline != NULL && pipeline_is_empty(new_pipeline) && pipeline_get_wait(new_pipeline));
    return new_pipeline;
}
/*
 * Nuevo `pipeline', sin comandos simples y establecido para que espere.
 *   Returns: nuevo pipeline sin comandos simples y que espera.
 * Ensures: result != NULL
 *  && pipeline_is_empty(result)
 *  && pipeline_get_wait(result)
 */

pipeline pipeline_destroy(pipeline self){
    
    assert(self!=NULL);
    g_list_free_full(self->commands, (GDestroyNotify)scommand_destroy_void);
    free(self);
    self=NULL;
    assert(self==NULL);
    return self;
}
/*
 * Destruye `self'.
 *   self: tubería a a destruir.
 * Requires: self != NULL
 * Ensures: result == NULL
 */

/* Modificadores */

void pipeline_push_back(pipeline self, scommand sc)
/*
 * Agrega por detrás un comando simple a la secuencia.
 *   self: pipeline al cual agregarle el comando simple.
 *   sc: comando simple a agregar. El TAD se apropia del comando.
 * Requires: self!=NULL && sc!=NULL
 * Ensures: !pipeline_is_empty()
 */
{
    assert((self != NULL) && (sc != NULL));
    self->commands = g_list_append(self->commands, sc);
    assert(!pipeline_is_empty(self));
    
 }

void pipeline_pop_front(pipeline self)
/*
 * Quita el comando simple de adelante de la secuencia.
 *   self: pipeline al cual sacarle el comando simple del frente.
 *      Destruye el comando extraido.
 * Requires: self!=NULL && !pipeline_is_empty(self)
 */
{
    assert(self != NULL && !pipeline_is_empty(self));
    self->commands = g_list_remove(self->commands,pipeline_front(self));
}

void pipeline_set_wait(pipeline self, const bool w)
/*
 * Define si el pipeline tiene que esperar o no.
 *   self: pipeline que quiere ser establecido en su atributo de espera.
 * Requires: self!=NULL
 */
{
    assert(self != NULL);
    self->background = w;
}

/* Proyectores */

bool pipeline_is_empty(const pipeline self){
    assert(self != NULL);
    return (self->commands == NULL);
}
/*
 * Indica si la secuencia de comandos simples tiene longitud 0.
 *   self: pipeline a decidir si está vacío.
 *   Returns: ¿Está vacío de comandos simples el pipeline?
 * Requires: self!=NULL
 */

unsigned int pipeline_length(const pipeline self){
    assert(self != NULL);
    unsigned int result;
    if(self->commands == NULL){
        result = 0;
    }else{
        result =g_list_length(self->commands);
    }
    assert((result==0) == pipeline_is_empty(self));
    return result;
}
/*
 * Da la longitud de la secuencia de comandos simples.
 *   self: pipeline a medir.
 *   Returns: largo del pipeline.
 * Requires: self!=NULL
 * Ensures: (pipeline_length(self)==0) == pipeline_is_empty()
 *
 */

scommand pipeline_front(const pipeline self){
    assert(self != NULL  && !pipeline_is_empty(self));
    scommand return_command = g_list_first(self->commands)->data;
    assert(return_command!=NULL);
    return return_command;
}
/*
 * Devuelve el comando simple de adelante de la secuencia.
 *   self: pipeline al cual consultar cual es el comando simple del frente.
 *   Returns: comando simple del frente. El comando devuelto sigue siendo
 *      propiedad del TAD.
 *      El resultado no es un "const scommand" ya que el llamador puede
 *      hacer modificaciones en el comando, siempre y cuando no lo destruya.
 * Requires: self!=NULL && !pipeline_is_empty(self)
 * Ensures: result!=NULL
 */

bool pipeline_get_wait(const pipeline self){
    assert(self != NULL);
    return self->background;
}
/*
 * Consulta si el pipeline tiene que esperar o no.
 *   self: pipeline a decidir si hay que esperar.
 *   Returns: ¿Hay que esperar en el pipeline self?
 * Requires: self!=NULL
 */

char * pipeline_to_string(const pipeline self){
    assert(self != NULL);
    

    //Caso pipeline Vacia
    if(pipeline_is_empty(self)){
        return g_strdup("");
    }



    GString *pipe_str = g_string_new(NULL);
    GList *current = self->commands;
    bool first_command = true;



    while(current != NULL){
        scommand temp = (scommand)current->data;

        //Primer comando en pipe
        if(first_command){
            first_command = false;
        }else{
            g_string_append(pipe_str, " | ");
        }


        //Convierte scommand a string y añade al resultado
        char *cmd_str = scommand_to_string(temp);
        g_string_append(pipe_str, cmd_str);
        g_free(cmd_str);                                  //Libera memoria (que no se rompa por cuarta vez)


        //Iterador
        current = g_list_next(current);
    }



    if(!pipeline_get_wait(self)){
        g_string_append(pipe_str, " &");
    }

    char *result = g_string_free(pipe_str, FALSE);          //g_string_free asegura condicion del llamador
    assert(pipeline_is_empty(self) || pipeline_get_wait(self) || strlen(result)>0);
    return result;
}
/* Pretty printer para hacer debugging/logging.
 * Genera una representación del pipeline en una cadena (aka "serializar").
 *   self: pipeline a convertir.
 *   Returns: una cadena con la representación del pipeline similar
 *     a lo que se escribe en un shell. Debe destruirla el llamador.
 * Requires: self!=NULL
 * Ensures: pipeline_is_empty(self) || pipeline_get_wait(self) || strlen(result)>0
 */