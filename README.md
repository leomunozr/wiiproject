wiiproject
==========
Juego de Snake para Raspberry Pi utilizando un control Wii Nunchuck

El juego consiste en controlar una serpiente con el joystick del control para llevarla hacia la comida y hacer que crezca. Si la serpiente llegara a chocar consigo misma el juego termina.

Para poder utilizar el control Wii Nunchuck con la Raspberry Pi se debe configurar el puerto I2C, instalar los módulos de Python par su uso y habilitarlos para que sean cargados al inicial la Raspberry Pi. Todo esto se puede hacer utilizando el script configuracion.sh, o bien, por medio del comando *make* en la carpeta raíz. La instalación requiere de permisos de administrador, por lo que es necesario ejecutar el script con permisos sudo.

Para ver un video demostrativo de este proyecto ve a:
http://bit.ly/1F4Kg6V

Cualquier tema realcionado con este proyecto puede contactar con el autor:
	Leonardo Muñoz
* leonardomr1@gmail.com

Docs
----
Para ver una referencia de los objetos ir a: http://wiiproject.rtfd.org

Schematics
----------
Las conexiones necesarias para armar el proyecto se muestran [aqui](schematics/)
