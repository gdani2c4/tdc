# tdc - traducción de archivos de programación

el comando tdc traduce ARCHIVO(s) contra una lista de
traducciones de fichas léxicas (cadenas, comentarios,
nombres de variables) que están para traducir
en ARCHIVO(s).


## instalación

la fuente del programa se encuentra enteramente en
*tdc.py*. Antes pasar el archivo al intérprete de
*python3* hay que cambiar tabulaciones a espacios,
lo que se puede cumplir mediante:

`sed -i 's/\t/\o040\o040\o040\o040/' tdc.py`

## guía del uso

- nota: se supone que la terminal está en el directorio raíz
  (es decir, que `$PWD` lleva tal valor) del programa
  que está para traducir

1. tcd supone que se encuentra un archivo *dat/tdc.json*
  de la forma:

    `{`

    `"cda": {[`CADENA`: `TRADUCCIÓN[`,` ...]]`},`

    `"abrv": {[`CADENA`: `TRADUCCIÓN[`,` ...]]`}`

    `}`

    - el lector puede dejar los valores de "cda" y
      "abrv" diccionarios json vacíos - al crear *tdc.json*
      se rellena en el paso siguiente.

2. `tdc -a ARCHIVO...`

    actualizará la lista de traduccion. Eso es, se unan las
    fichas nuevas de ARCHIVO(s) y se eliminan aquellas que ya
    no se encuentran. El *tdc.json* anterior queda
    guardada como *tdc.json*[FECHA], con la FECHA y hora
    actual

3. hay que agregar las traducciones a mano, las que quedan
   vacías no se tratan y se quedan tales como salen en
   ARCHIVO

    - bajo la llave *abrv* van los nombres o
      partes de nombres / abreviaturas que están para
      traducir.

    nota: esta primera versión sufre de remplazos
    anidados, ve problema nº 1

4. `tdc -t ARCHIVO ...`

    aplica la lista de traducción *dat/tdc.json* a
    ARCHIVO(s) *CAMINO/NOMBRE* y las guarda en 
    *CAMINO/EN/NOMBRE*. Si no existe el subdirectorio 
    *EN* se crea.
