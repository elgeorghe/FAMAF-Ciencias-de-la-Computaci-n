#include <stdlib.h>
#include <stdbool.h>

#include "parsing.h"
#include "parser.h"
#include "command.h"

static scommand parse_scommand(Parser p) {
    arg_kind_t arg_type;
    bool has_input = false, has_output = false, error = false;
    

    scommand result = scommand_new();
    char *arg = parser_next_argument(p, &arg_type);
    
    while(!parser_at_eof(p) && !error){
        
        if (arg == NULL){
                free(arg);
                return result;
            }
        parser_skip_blanks(p);
        
        if(arg_type == ARG_NORMAL){
            scommand_push_back(result, arg);
        }else if(arg_type == ARG_INPUT){
            //Redireccion de Input
            if(has_input){
                error = true;
            }
            
            scommand_set_redir_in(result, arg);
            has_input = true;                               //Mybash no permite multiples inputs
        
        }else if(arg_type == ARG_OUTPUT){
            //Redireccion de Output
            if(has_output){
                error = true;
            }
            scommand_set_redir_out(result, arg);
            has_output = true;                              //Mybash no permite multiples outputs
        }

        arg = parser_next_argument(p, &arg_type);
    }
    
    //EMPTY RETURN
    if(!error && scommand_length(result) == 0){
        if(arg_type == ARG_INPUT || arg_type == ARG_OUTPUT){
            result = scommand_destroy(result);
            result = NULL;
            return result;
        }else if(arg_type == ARG_NORMAL){
            scommand_push_back(result, arg);
        }else if(arg == NULL){
            free(arg);
            return result;
        }
    }

    //ERROR NULL RETURN
    if(error){
        result = scommand_destroy(result);
        result = NULL;
        return result;
    }

    
    free(arg);
    return result;
}

pipeline parse_pipeline(Parser p) {
    pipeline result = pipeline_new();
    scommand cmd = NULL;
    bool error = false, another_pipe=true, background = false, basura = false;

    

    while (another_pipe && !error && !parser_at_eof(p)) {
        cmd = parse_scommand(p);
        if(cmd != NULL){
            pipeline_push_back(result, cmd);
            parser_op_pipe(p, &another_pipe);
        }else{
            error = true;
        }
    }
    
    //BACKGROUND OP HANDLING
    if(!parser_at_eof(p)){
        parser_op_background(p, &background);
        if(background){
            pipeline_set_wait(result, !background);
        }
    }
    
    
    //consumir '\n'
    if (!parser_at_eof(p)) {
        parser_garbage(p, &basura);
        if(basura){
            printf("basura : %s\n", parser_last_garbage(p));
        }
    }

    //ERROR HANDLING
    if(error || basura){
        cmd = scommand_destroy(cmd);
        result = pipeline_destroy(result);
        result = NULL;
    }

    return result; 
}

