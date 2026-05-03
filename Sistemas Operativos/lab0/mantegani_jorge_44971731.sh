#!/bin/bash

# EJERCICIO 1: Modelo del procesador
grep "model name" /proc/cpuinfo | uniq

# EJERCICIO 2: Número de unidades de ejecución (cores)
grep "model name" /proc/cpuinfo | wc -l

# EJERCICIO 3: Lista de nombres de usuarios para red social de superhéroes
curl -O https://raw.githubusercontent.com/dariomalchiodi/superhero-datascience/master/content/data/heroes.csv | cut -d ";" -f 2 heroes.csv | tr ' ' '_' | sed '/^$/d' > salida.txt

# EJERCICIO 4A: Día de máxima temperatura en Córdoba
sort -k5 -n -r datos/weather_cordoba.in | awk '{print $1, $2, $3}' | head -1

# EJERCICIO 4B: Día de mínima temperatura en Córdoba
sort -k6 -n datos/weather_cordoba.in | awk '{print $1, $2, $3}' | head -1

# EJERCICIO 5: Ordenar jugadores de tenis por ranking
sort -k3 -n datos/atpplayers.in

# EJERCICIO 6: Ordenar tabla de Superliga por puntos y diferencia de goles
awk '{dg = $7 - $8; print $0, dg}' datos/superliga.in | sort -k2,2nr -k9,9nr

# EJERCICIO 7: MAC address de la placa WiFi del equipo
ip addr | grep ether | awk '{print $2}'

# EJERCICIO 8: Renombrar archivos de subtítulos
for i in {1..10}; do printf -v num "%02d" $i; mv "serie_prueba/fma_s01E${num}_es.srt" "serie_prueba/fma_s01E${num}.srt"; done

# EJERCICIO 9A: Recortar video con ffmpeg
ffmpeg -i video.mp4 -ss 3 -t 9 -c copy video_recortado.mp4

# EJERCICIO 9B: Mezclar audio con ffmpeg
ffmpeg -i voz.wav -i musica.mp3 -filter_complex "amix=inputs=2:duration=shortest:dropout_transition=2" salida.mp3

