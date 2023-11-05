# Tp1-PLN
Primer Trabajo Práctico de Procesamiento del Lenguaje Natural

En el archivo ipynb se encuentra la resolucion del TP1.

El resto de los archivos son para el funcionamiento del Bot de Telegram sugerido como desafío opcional.
Para facilitar su uso decidimos crear 2 csv, generados por el codigo del TP1 para minimizar el procesamiento y complejidad del bot.
Los mismos corresponden al dia 3/11/23 por lo que pueden diferir de los resultados de la notebook actuales.

Para correr el bot localmente deben instalar los modulos detallados en el req.txt
```bash
pip install -r req.txt
```
Se debe añadir el token de telegram en el config.py

Luego ejecutar el archivo
```bash
python telegram_bot_py
```
Con el bot corriendo se puede entablar una coneccion mediante su nombre
@TUIA_PNL_BOT

El bot dispone de una serie de comandos:
/start : mensaje bienvenida
/about : datos acerca del bot
/resumen: presenta las opciones via teclado para elegir la categoria de la cual se desea tener el resumen de noticias
/ia,/cyc,/medicina/,/pc: listan las noticias de la categoria, mandando el nro de la noticias nos da el cuerpo de la misma


Integrantes:
Di Marco, Nicolas
Escandell, Ariel
Raffaeli, Taiel
