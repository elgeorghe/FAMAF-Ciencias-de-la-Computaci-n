	.equ SCREEN_WIDTH,   640
	.equ SCREEN_HEIGH,   480
	.equ BITS_PER_PIXEL, 32

	.equ GPIO_BASE,    0x3f200000
	.equ GPIO_GPFSEL0, 0x00
	.equ GPIO_GPLEV0,  0x34

	

	.globl main

//variables usadas
//x0, señala el pixel que voy a pintar, x20 guarda el pixel inicial
//x1,x2,x3,x4,x5,x6,x7,x8,x16 las usamos en las funciones de circulo y/o cuadrado
//x9 guarda enteros para las funciones que no te dejan usarlos
//x10 guarda el color con el que vas a pintar
//x11 se usa en el gpio para comparar las teclas
//x12,x13,x26 se usan para el delay. El delay inicial se guarda en x14
//x14 se usa en el gpio 
//x15 se fija cuando desaceleras cual era el sentido en que ibas antes
//x17,x18 se usan para ver si ganaste o perdiste el juego, uno se usa para ver el color del pixel al que te moves y otro para ver el color del pixel de ganar o perder
//x21,x22,x23 guardan el lado del cuadrado principal para la animacion y sus coordenadas de inicio

main:
	mov x20, x0 // Guarda la dirección base del framebuffer en x20 
	//---------------- CODE HERE ------------------------------------

	movz x10, 0x00, lsl 16
	movk x10, 0x0000, lsl 00


	mov x15,3
	movz x12, 0x10F, lsl 16 //ESTE ES EL DELAY
	movk x12, 0xF000, lsl 00

	mov x26,x12
	
	mov x2, SCREEN_HEIGH         // Y Size




//----------------------------------------------------------------------- fondo fondo




empezar_fondo:

	mov x12,x26
	mov x2, SCREEN_HEIGH         // Y Size
	mov x10,0
	movz x10, 0x00, lsl 16
	movk x10, 0x0000, lsl 00
	mov x0,x20


aux_fondo:
	mov x1, SCREEN_WIDTH         // uso para pintar el fondo (largo)
fondo:
	stur w10,[x0]  // Colorear el pixel N
	add x0,x0,4    // Siguiente pixel
	sub x1,x1,1    // Decrementar contador tamaño total (largo)
	cbnz x1,fondo  // Si no terminó la fila, salto
	sub x2,x2,1    // Decrementar contador tamaño total (alto)
	cbnz x2,aux_fondo  // Si no es la última fila, salto







//----------------------cuadrado y obstaculos----------------------------------

//para el cuadrado-> x1 largo del cuadrado,x2 alto del cuadrado,x3 coordenada y del cuadrado,x4 coordenada x del cuadrado (coordenadas de la esquina superior izquierda)
//para el circulo-> x1 radio del circulo,x2 coordenada y del centro del circulo,x3 coordenada x del centro del circulo,x4 uso toda la pantalla de alto para ver si pinto o no el pixel,x5 uso toda la pantalla de largo para ver si pinto o no el pixel

objects:
	
	mov x0,x20
	
	mov x10, 0
	movz x10, 0xFF, lsl 16 //color color cuadrado
	movk x10, 0xFFFF, lsl 00 //color del cuadrado
	mov x23,10 
	mov x1, x23 
	mov x2, x23 
	mov x3, 450
	mov x22,x3
	mov x4,10 
	mov x21,x4
	bl empezar_cuadrado

	mov x10, 0
	movz x10, 0xFF, lsl 16 //color rojo
	movk x10, 0x0000, lsl 00 //color rojo
	
	mov x0,x20
	mov x1,640
	mov x2,3
	mov x3,1
	mov x4,1
	bl empezar_cuadrado

	mov x0,x20
	mov x1,640
	mov x2,3
	mov x3,477
	mov x4,1
	bl empezar_cuadrado

	mov x0,x20
	mov x1,3
	mov x2,480
	mov x3,1
	mov x4,1
	bl empezar_cuadrado

	mov x0,x20
	mov x1,3
	mov x2,480
	mov x3,1
	mov x4,637
	bl empezar_cuadrado

	mov x0,x20
	mov x1,240
	mov x2,240
	mov x3,240
	mov x4,200
	bl empezar_cuadrado

	mov x0,x20
	mov x1,220
	mov x2,150
	mov x3,20
	mov x4,20
	bl empezar_cuadrado

	mov x0,x20
	mov x1,80
	mov x2,50
	mov x3,3
	mov x4,280
	bl empezar_cuadrado

	mov x0,x20
	mov x1,60
	mov x2,80
	mov x3, 170
	mov x4,345
	bl empezar_cuadrado

	mov x0,x20
	mov x1,180
	mov x2,60
	mov x3,80
	mov x4,420
	bl empezar_cuadrado

	mov x0,x20
	mov x1,25
	mov x2,60
	mov x3,80
	mov x4,611
	bl empezar_cuadrado

	mov x0,x20
	mov x1,80
	mov x2,30
	mov x3,235
	mov x4,465
	bl empezar_cuadrado

	mov x0,x20
	mov x1,100
	mov x2,30
	mov x3,300
	mov x4,490
	bl empezar_cuadrado

	mov x0,x20
	mov x1,80
	mov x2,30
	mov x3,350
	mov x4,440
	bl empezar_cuadrado

	mov x0,x20
	mov x1,10
	mov x2,320
	mov x3,80
	mov x4,590
	bl empezar_cuadrado

	mov x0,x20
	mov x1,30 
	mov x2,215 
	mov x3,230 
	mov x4,SCREEN_HEIGH 
	mov x5,SCREEN_WIDTH 
 	bl circulo_aux

	mov x0,x20
	mov x1,40  
	mov x2,115  
	mov x3,310  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	mov x0,x20
	mov x1,30  
	mov x2,185  
	mov x3,455  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	mov x0,x20
	mov x1,30  
	mov x2,185  
	mov x3,545  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	mov x0,x20
	mov x1,30  
	mov x2,420  
	mov x3,560  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	mov x0,x20
	mov x1,4  
	mov x2,240  
	mov x3, 620 
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux


	mov x10,0
	movz x10, 0xFF, lsl 16 //color amarillo
	movk x10, 0xFF00, lsl 00 //color amarillo

	mov x0,x20
	mov x1,13  
	mov x2,180  
	mov x3, 620 
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	

	b quieto

quieto:
	bl gpio
	b quieto




// -----------------funcion para hacer cuadrados-----------------------------------


empezar_cuadrado:
	add x0,x0,2560 //avanza 640 pixeles,es decir una linea
	sub x3,x3,1	
	cbnz x3,empezar_cuadrado //mientras no llegues a la coordenada y que queres saltas una linea
	mov x9,4
	mul x4,x4,x9
	add x0,x0,x4 //le sumo la coordenada x
	mov x5,x1
	b cuadrado
aux_cuadrado:
	mov x5, x1         // cuadrado (largo)
	mov x9,4
	mul x6,x9,x5
	mov x9,2560
	sub x6,x9,x6
	add x0,x0,x6 //todo esto es para hacer el salto a la siguiente linea del cuadrado
	b cuadrado
	
cuadrado:
	stur w10,[x0]  // Colorear el pixel N
	add x0,x0,4    // Siguiente pixel
	sub x5,x5,1    // Decrementar contador tamaño cuadrado(largo)
	cbnz x5,cuadrado  // Si no terminó la fila, salto
	sub x2,x2,1    // Decrementar tamaño cuadrado (alto)
	cbnz x2,aux_cuadrado  // Si no es la última fila, salto

	
ret


//-------------------------funcion para hacer circulos


circulo:
	sub x6,x0,x20
	mov x9,4
	sdiv x6,x6,x9//x6 es el numero de pixel que estoy viendo
	mov x9,SCREEN_WIDTH
	sdiv x7,x6,x9//guardo coordenadaas alto de el pixel que estoy viendo
	mul x8,x7,x9 
	sub x8,x6,x8//guardo coordenadas largo de el pixel que estoy viendo
	
	sub x7,x7,x2//guardo la diferencia de las coordenadas en alto entre el pixel y el centro
	sub x8,x8,x3//guardo la diferencia de las coordenadas en largo entre el pixel y el centro

	mul x7,x7,x7 //dfierencia de alto al cuadrado
	mul x8,x8,x8 //diferencia de largo al cuadrado
	add x8,x7,x8 //suma de las diferencias al cuadrado
	mul x7,x1,x1 //radio al cuadrado


	cmp x8,x7

	b.le paint
	b.gt nopaint  

circulo_aux: 
	mov x16,x5
	b circulo
paint:
	stur w10,[x0]  // Colorear el pixel N
	add x0,x0,4    // Siguiente pixel
	sub x16,x16,1   
	cbnz x16,circulo 
	sub x4,x4,1
	cbnz x4,circulo_aux    
	ret
nopaint:
	add x0,x0,4
	sub x16,x16,1   
	cbnz x16,circulo 
    sub x4,x4,1
	cbnz x4,circulo_aux
	ret

//en paint y no paint hago igual que en el fondo nomas que lo pinto o no segun corresponda
//--------------------gpio-------

gpio:	


	mov x9, GPIO_BASE 
	str wzr, [x9, GPIO_GPFSEL0]
	mov w14,0
	ldr w14, [x9, GPIO_GPLEV0]
	and w11, w14, 0b00000010 
	cbz w11, gpio2
	cbnz w11, abj_arr
	

gpio2:


	mov x9, GPIO_BASE
	str wzr, [x9, GPIO_GPFSEL0]
	mov w14,0
	ldr w14, [x9, GPIO_GPLEV0]
	and w11, w14, 0b00000100
	cbz w11, gpio3
	cbnz w11, der_izq

gpio3:

	mov x9, GPIO_BASE
	str wzr, [x9, GPIO_GPFSEL0]
	mov w14,0
	ldr w14, [x9, GPIO_GPLEV0]
	and w11, w14, 0b00001000
	cbz w11, gpio4
	cbnz w11, arr_abj

gpio4:

	mov x9, GPIO_BASE
	str wzr, [x9, GPIO_GPFSEL0]
	mov w14,0
	ldr w14, [x9, GPIO_GPLEV0]
	and w11, w14, 0x10
	cbz w11, gpio5
	cbnz w11, izq_der

gpio5:	
	mov x9, GPIO_BASE
	str wzr, [x9, GPIO_GPFSEL0]
	mov w14,0
	ldr w14, [x9, GPIO_GPLEV0]
	and w11, w14, 0x20
	cbnz w11, desacelerar
ret



//----------------------------------movimientos y animacion---------------------
desacelerar:
	mov x9,10
	sdiv x9,x12,x9
	add x12,x12,x9 //aumento el delay un 10%
	mov x9,1
	cmp x9,x15
	b.eq arr_abj //me fijo cual animacion estaba antes y continuo con esa
	mov x9,2
	cmp x9,x15
	b.eq izq_der
	mov x9,3
	cmp x9,x15
	b.eq abj_arr
	mov x9,4
	cmp x9,x15
	b.eq der_izq


	 
//-----------arriba_abajo

arr_abj:

	mov x13,x12	

	bl delay 

	mov x0,x20
	mov x1,x23
	mov x2,x23
	add x3,x22,1
	mov x4,x21
	mov x10, 0
	movz x10, 0xFF, lsl 16 //color cuadrado
	movk x10, 0xFFFF, lsl 00 //color cuadrado
	bl empezar_cuadrado_a 
	add x22,x22,1
	bl borrar_2 //hago un rectangulo del color del fondo que acabo de salir para que se borre el rastro del cuadrado
	bl gpio

	mov x15,1 //guardo  en x15 el numero de direccion este
	b arr_abj
	

borrar_2:
		
	sub SP,SP,8
	stur x30,[SP,0]
	mov x0,x20
	mov x1,x23
	mov x2,1
	sub x3,x22,1
	mov x4,x21
	mov x10, 0
	movz x10, 0x00, lsl 16 
	movk x10, 0x0000, lsl 00 
	bl empezar_cuadrado_a
	ldr x30, [SP, 0]					
	add SP, SP, 8	
	ret




//--------------izquierda derecha


izq_der:

	mov x13,x12	
	
	bl delay

	mov x0,x20
	mov x1,x23
	mov x2,x23
	mov x3,x22
	add x4,x21,1
	mov x10, 0
	movz x10, 0xFF, lsl 16 //color xuadrado
	movk x10, 0xFFFF, lsl 00 //color cuadrado
	bl empezar_cuadrado_a
	add x21,x21,1
	bl borrar
	bl gpio

	mov x15,2 //guardo  en x15 el numero de direccion este
	b izq_der
	

borrar:
	sub SP,SP,8
	stur x30,[SP,0]
	mov x0,x20
	mov x1,1
	mov x2,x23
	mov x3,x22
	sub x4,x21,1
	mov x10, 0
	movz x10, 0x00, lsl 16 
	movk x10, 0x0000, lsl 00 
	bl empezar_cuadrado_a
	ldr x30, [SP, 0]					
	add SP, SP, 8	
	ret

//--------------abajo arriba
abj_arr:
	//le deberia pasar la posicion del cuadrado

	mov x13,x12	
	
	bl delay

	mov x0,x20
	mov x1,x23
	mov x2,x23
	sub x3,x22,1
	mov x4,x21
	mov x10, 0
	movz x10, 0xFF, lsl 16  //color cuadrado
	movk x10, 0xFFFF, lsl 00  //color cuadrado
	bl empezar_cuadrado_a
	sub x22,x22,1
	bl borrar_3
	bl gpio

	mov x15,3 //guardo  en x15 el numero de direccion este
	b abj_arr
	

borrar_3:
	sub SP,SP,8
	stur x30,[SP,0]
	mov x0,x20
	mov x1,x23
	mov x2,1
	add x3,x22,x23
	mov x4,x21
	mov x10, 0
	movz x10, 0x00, lsl 16 
	movk x10, 0x0000, lsl 00 
	bl empezar_cuadrado_a
	ldr x30, [SP, 0]					
	add SP, SP, 8	
	ret


//-------------------------------derecha izquierda
der_izq:

	mov x13,x12
	
	bl delay

	mov x0,x20
	mov x1,x23
	mov x2,x23
	mov x3,x22
	sub x4,x21,1
	mov x10, 0
	movz x10, 0xFF, lsl 16 //color cuadrado
	movk x10, 0xFFFF, lsl 00 //color cuadrado
	bl empezar_cuadrado_a
	sub x21,x21,1
	bl borrar_4
	bl gpio

	mov x15,4 //guardo  en x15 el numero de direccion este
	b der_izq
	

borrar_4:
	sub SP,SP,8
	stur x30,[SP,0]
	mov x0,x20
	mov x1,1
	mov x2,x23
	mov x3,x22
	add x4,x21,x23
	mov x10, 0
	movz x10, 0x00, lsl 16 //color pasto
	movk x10, 0x0000, lsl 00 //color pasto
	bl empezar_cuadrado_a
	ldr x30, [SP, 0]					
	add SP, SP, 8	
	ret

//-------------------------------cuadrados que pueden ganar!!!!.... y morir-------------------------
empezar_cuadrado_a: //esta funcion es similar a empezar cuadrado con la particualaridad que se fija si puede o no morir/ganar 
		

	add x0,x0,2560 
	sub x3,x3,1	
	cbnz x3,empezar_cuadrado_a
	mov x9,4
	mul x4,x4,x9
	add x0,x0,x4
	mov x5,x1
	b cuadrado_a
aux_cuadrado_a:
	mov x5, x1         // cuadrado (largo)
	mov x9,4
	mul x6,x9,x5
	mov x9,2560
	sub x6,x9,x6
	add x0,x0,x6 //todo esto es para hacer el salto a la siguiente linea del cuadrado
	b cuadrado_a
	
cuadrado_a:
 	sub SP,SP,8
	stur x30,[SP,0] 
	bl morir //me fijo si  muero
	ldr x30, [SP, 0]					
	add SP, SP, 8	
 	
	sub SP,SP,8
	stur x30,[SP,0] 
	bl ganar //me fijo si gano
	ldr x30, [SP, 0]					
	add SP, SP, 8
	
	stur w10,[x0]  // Colorear el pixel N
	add x0,x0,4    // Siguiente pixel
	sub x5,x5,1    // Decrementar contador tamaño cuadrado(largo)
	cbnz x5,cuadrado_a  // Si no terminó la fila, salto
	sub x2,x2,1    // Decrementar tamaño cuadrado (alto)
	cbnz x2,aux_cuadrado_a  // Si no es la última fila, salto


ret

//--------------morir

 morir:
	ldur w17,[x0]
	mov x18,0
	movz x18, 0xFF, lsl 16
	movk x18, 0x0000, lsl 00
	cmp x17,x18 //comparo el color en el pixel con el color rojo
	b.eq empezar_fondo //si son iguales voy al principio
ret

//-----------------ganar----

 ganar:
	ldur w17,[x0]
	mov x18,0
	movz x18, 0xFF, lsl 16
	movk x18, 0xFF00, lsl 00
	cmp x17,x18 //comparo el color en el pixel con el color amarillo
	b.eq final //si son iguales gana el juego
ret
 

 //----------------------ganaste!!!!!---------

 final:
	mov x0,x20

	mov x10,0
	movz x10, 0x00, lsl 16
	movk x10, 0x0000, lsl 00

	mov x2,SCREEN_HEIGH
	b aux_fondo_final

	

aux_fondo_final:
	mov x1, SCREEN_WIDTH         // uso para pintar el fondo (largo)

fondo_final:
	stur w10,[x0]  // Colorear el pixel N
	add x0,x0,4    // Siguiente pixel
	sub x1,x1,1    // Decrementar contador tamaño total (largo)
	cbnz x1,fondo_final  // Si no terminó la fila, salto
	sub x2,x2,1    // Decrementar contador tamaño total (alto)
	cbnz x2,aux_fondo_final  // Si no es la última fila, salto
	b carita_feliz

carita_feliz:
	mov x0,x20


//-------ojo_izquierdo------------------------------------------
	mov x10, 0
	movz x10, 0xFF, lsl 16 
	movk x10, 0xFFFF, lsl 00 
	mov x1, 36 
	mov x2, 36 
	mov x3, 109 
	mov x4, 146 
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,73
	mov x4,146
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,145
	mov x4,182
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,145
	mov x4,218
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,37
	mov x4,182
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,37
	mov x4,218
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,73
	mov x4,254
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,109
	mov x4,254
	bl empezar_cuadrado
	
//-------ojo_derecho------------------------------------------

	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,106
	mov x4,346
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,73
	mov x4,346
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,145
	mov x4,382
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,145
	mov x4,418
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,37
	mov x4,382
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,37
	mov x4,418
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,73
	mov x4,454
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,109
	mov x4,454
	bl empezar_cuadrado
	
//-------------boca-------------------

	mov x0,x20
	mov x1,480
	mov x2,36
	mov x3,240
	mov x4,80
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,276
	mov x4,80
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,312
	mov x4,116
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,348
	mov x4,152
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,384
	mov x4,188
	bl empezar_cuadrado
	
//-----parte_derecha

	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,276
	mov x4,524
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,312
	mov x4,488
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,348
	mov x4,452
	bl empezar_cuadrado
	
	mov x0,x20
	mov x1,36
	mov x2,36
	mov x3,384
	mov x4,416
	bl empezar_cuadrado
	
//-----rectangulo-abajo

	mov x0,x20
	mov x1,196
	mov x2,36
	mov x3,400
	mov x4,224
	bl empezar_cuadrado


//-----------------------delay
delay:
	sub x13,x13,1
   	cbnz x13,delay
	ret



InfLoop:

	b InfLoop
