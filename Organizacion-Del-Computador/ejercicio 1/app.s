	.equ SCREEN_WIDTH,   640
	.equ SCREEN_HEIGH,   480
	.equ BITS_PER_PIXEL, 32

	.equ GPIO_BASE,    0x3f200000
	.equ GPIO_GPFSEL0, 0x00
	.equ GPIO_GPLEV0,  0x34

	.globl main

main:
	// x0 contiene la direccion base del framebuffer
	mov x20, x0 // Guarda la dirección base del framebuffer en x20
	//---------------- CODE HERE ------------------------------------

	movz x10, 0x0B, lsl 16 //color cielo
	movk x10, 0xF2F2, lsl 00 //color cielo


	mov x2,SCREEN_HEIGH // uso para pintar fondo (alto)

	

//----------------------------------------------------------------------- cielo

aux_fondo:
	mov x1, SCREEN_WIDTH         // uso para pintar el fondo (largo)
fondo:
	stur w10,[x0]  // Colorear el pixel N
	add x0,x0,4    // Siguiente pixel
	sub x1,x1,1    // Decrementar contador tamaño total (largo)
	cbnz x1,fondo  // Si no terminó la fila, salto
	sub x2,x2,1    // Decrementar contador tamaño total (alto)
	cbnz x2,aux_fondo  // Si no es la última fila, salto

//--- objects
//cualquier figura x10->color,x0->x20 para arrancar desde el principio
//cuadrados: x1->largo del cuadrado. x2->alto del cuadrado. x3->coordenada y del cuadrado. x4->coordenada x del cuadrado
//circulos: x1->radio del circulo. x2->coordenada y del centro del circulo.x3->coordenada x del centro del circulo.x4,x5->uso para recorrer la pantalla 
objects:
	mov x0,x20
	mov x10, 0
	movz x10, 0x68, lsl 16 
	movk x10, 0xF545, lsl 00 
	mov x1, 640 
	mov x2, 80 
	mov x3, 400 
	mov x4, 1 
	bl empezar_cuadrado	


	mov x0,x20
	mov x10, 0
	movz x10, 0x42, lsl 16  
	movk x10, 0x4342, lsl 00  
	mov x1, 100  
	mov x2, 220  
	mov x3, 180  
	mov x4, 500  
	bl empezar_cuadrado

	mov x0,x20
	mov x10, 0
	movz x10, 0x42, lsl 16  
	movk x10, 0x4342, lsl 00  
	mov x1, 100  
	mov x2, 220  
	mov x3, 180  
	mov x4, 40  
	bl empezar_cuadrado


	mov x0,x20
	mov x10, 0
	movz x10, 0x81, lsl 16  
	movk x10, 0x2389, lsl 00  
	mov x1,100  
	mov x2,260  
	mov x3,320  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	mov x0,x20
	mov x10, 0
	movz x10, 0x33, lsl 16  
	movk x10, 0x99FF, lsl 00  
	mov x1,40  
	mov x2,260  
	mov x3,320  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	mov x0,x20
	mov x10, 0
	movz x10, 0xDC, lsl 16  
	movk x10, 0xDCDC, lsl 00  
	mov x1, 360  
	mov x2, 150  
	mov x3, 250  
	mov x4, 140  
	bl empezar_cuadrado

	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1,35  
	mov x2,300  
	mov x3,320  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux


	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1, 70  
	mov x2, 100  
	mov x3, 300  
	mov x4, 285  
	bl empezar_cuadrado


	mov x0,x20
	mov x10, 0
	movz x10, 0xFF, lsl 16 
	movk x10, 0xFFFF, lsl 00 
	mov x1, 1  
	mov x2, 135  
	mov x3, 265  
	mov x4, 320  
	bl empezar_cuadrado	

	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1, 30  
	mov x2, 30  
	mov x3, 150  
	mov x4, 570  
	bl empezar_cuadrado

	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1, 30  
	mov x2, 30  
	mov x3, 150  
	mov x4, 534  
	bl empezar_cuadrado

	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1, 30  
	mov x2, 30  
	mov x3, 150  
	mov x4, 500  
	bl empezar_cuadrado


	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1, 30  
	mov x2, 30  
	mov x3, 150  
	mov x4, 110  
	bl empezar_cuadrado


	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1, 30  
	mov x2, 30  
	mov x3, 150  
	mov x4, 74  
	bl empezar_cuadrado


	mov x0,x20
	mov x10, 0
	movz x10, 0xEC, lsl 16  
	movk x10, 0x7907, lsl 00  
	mov x1, 30  
	mov x2, 30  
	mov x3, 150  
	mov x4, 40  
	bl empezar_cuadrado


	mov x0,x20
	mov x10, 0
	movz x10, 0xFF, lsl 16  
	movk x10, 0x0000, lsl 00  
	mov x1,3  
	mov x2,350  
	mov x3,305  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux

	mov x0,x20
	mov x10, 0
	movz x10, 0xFF, lsl 16  
	movk x10, 0x0000, lsl 00  
	mov x1,3  
	mov x2,350  
	mov x3,335  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux


	mov x0,x20
	mov x10, 0
	movz x10, 0xFF, lsl 16  
	movk x10, 0xFF00, lsl 00  
	mov x1,40  
	mov x2,50  
	mov x3,405  
	mov x4,SCREEN_HEIGH  
	mov x5,SCREEN_WIDTH  
 	bl circulo_aux




	mov x9, GPIO_BASE
	str wzr, [x9, GPIO_GPFSEL0]

	b gpio


//-- hacer cuadrados


empezar_cuadrado:
	add x0,x0,2560 //avanza 640 pixeles,es decir una linea
	sub x3,x3,1	
	cbnz x3,empezar_cuadrado
	mov x9,4
	mul x4,x4,x9
	add x0,x0,x4
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

//--hacer circulos

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

	subs x17,x8,x7


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

//----------
	

aux_fondo_2:
	mov x1, SCREEN_WIDTH         // uso para pintar el fondo (largo)
	b fondo_2
fondo_2:
	ldur w13,[x0]  // Color del pixel N
	subs x17,x13,x14
	b.eq paint_2 
	b no_cielo


paint_2:
	stur w10,[x0]  // Colorear el pixel N
	add x0,x0,4    // Siguiente pixel
	sub x1,x1,1    // Decrementar contador tamaño total (largo)
	cbnz x1,fondo_2  // Si no terminó la fila, salto
	sub x2,x2,1    // Decrementar contador tamaño total (alto)
	cbnz x2,aux_fondo_2  // Si no es la última fila, salto   

	mov x10,0   
	movz x10, 0xFF, lsl 16  
	movk x10, 0xFFFF, lsl 00  
	mov x0,x20
	mov x1,50
	mov x2,40
	mov x3,300
	mov x4,SCREEN_HEIGH
	mov x5,SCREEN_WIDTH
	bl circulo_aux
no_cielo:
	subs x17,x13,x15
	b.eq paint_2
	b no_paint_2
no_paint_2:
	add x0,x0,4    // Siguiente pixel
	sub x1,x1,1    // Decrementar contador tamaño total (largo)
	cbnz x1,fondo_2  // Si no terminó la fila, salto
	sub x2,x2,1    // Decrementar contador tamaño total (alto)
	cbnz x2,aux_fondo_2  // Si no es la última fila, salto
	mov x10,0   
	movz x10, 0xFF, lsl 16  
	movk x10, 0xFFFF, lsl 00  
	mov x0,x20
	mov x1,50
	mov x2,40
	mov x3,300
	mov x4,SCREEN_HEIGH
	mov x5,SCREEN_WIDTH
	bl circulo_aux

//----------------------------

tecla_w:	
	mov x2, SCREEN_HEIGH
	mov x10,0
	mov x0,x20
	movz x10, 0x00, lsl 16  
	movk x10, 0x0000, lsl 00  
	movz x14, 0x0B, lsl 16 //color cielo
	movk x14, 0xF2F2, lsl 00 //color cielo
	movz x15, 0xFF, lsl 16  
	movk x15, 0xFF00, lsl 00  
	b aux_fondo_2
	

gpio:	
	ldr w10, [x9, GPIO_GPLEV0]
	and w11, w10, 0b00000010
	cbz w11, gpio
	bl tecla_w


InfLoop:
	b InfLoop


