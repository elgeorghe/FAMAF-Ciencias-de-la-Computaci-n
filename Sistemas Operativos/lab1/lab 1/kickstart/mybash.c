#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "command.h"
#include "execute.h"
#include "parser.h"
#include "parsing.h"
#include "builtin.h"

static void show_prompt(void) {
    printf ("mybash> ");
    fflush (stdout);
}

int main(int argc, char *argv[]) {
    pipeline pipe;
    Parser input;
    bool quit = false;

    input = parser_new(stdin);
    while (!quit) {
        show_prompt();
        pipe = parse_pipeline(input);

        /* Hay que salir luego de ejecutar? */
        quit = parser_at_eof(input);
        
        printf("soy interno? %d, el pipe es %d largo, y yo soy %s \n",builtin_is_internal(pipeline_front(pipe)),pipeline_length(pipe),scommand_to_string(pipeline_front(pipe)));

        execute_pipeline(pipe);
    }
    parser_destroy(input); input = NULL;
    return EXIT_SUCCESS;
}

