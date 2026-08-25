# Lab-1-Vision-Por-Computador

# Reto: Seguimiento de figura en video

## Análisis de Resultados y Conclusiones

### Sobre la captura y el procesamiento de la imagen

El reto se implementó en Python utilizando OpenCV y NumPy. El programa puede obtener imágenes desde la cámara del computador y convertir cada cuadro capturado desde el espacio de color BGR al espacio HSV. Esta conversión facilita la segmentación, ya que permite separar el tono del color de su saturación y brillo.

Para la primera ejecución se seleccionó únicamente el color rojo. De esta manera, el algoritmo analiza la imagen buscando solamente los píxeles que pertenecen a ese color, sin procesar todavía las figuras verdes o azules.

### Sobre la segmentación del color rojo

La segmentación se realizó mediante la función `cv2.inRange()`, comparando cada píxel de la imagen con un rango HSV previamente definido:

```python
bajo1 = [0, 120, 70]
alto1 = [10, 255, 255]
```

El rojo requiere un tratamiento especial porque se encuentra en los extremos del canal Hue. Por esta razón, también se utiliza un segundo rango:

```python
bajo2 = [170, 120, 70]
alto2 = [180, 255, 255]
```

Ambas máscaras se combinan mediante una operación OR. Esto permite detectar tanto los rojos cercanos a 0 grados como los rojos cercanos a 180 grados. En la imagen de prueba, el rectángulo rojo presenta un tono intenso y una saturación alta, por lo que se encuentra dentro de los rangos definidos.

El resultado de la segmentación es una máscara binaria: los píxeles identificados como rojos aparecen en blanco y el resto de la imagen aparece en negro. Por lo tanto, el rectángulo rojo queda aislado, mientras que el fondo blanco y las figuras verde y azul son ignorados.

### Sobre la limpieza de la máscara

Después de crear la máscara, se aplicaron operaciones morfológicas utilizando un kernel de tamaño 5x5. Primero se realiza una erosión para eliminar pequeños puntos de ruido y posteriormente una dilatación para recuperar y unir las regiones correspondientes a la figura.

Este procedimiento permite obtener una región más uniforme y evita que pequeñas imperfecciones de la cámara, reflejos o variaciones de iluminación sean interpretadas como objetos independientes.

### Sobre la detección de la figura

Una vez obtenida la máscara limpia, se buscaron los contornos externos mediante `cv2.findContours()`. De todos los contornos encontrados se seleccionó el de mayor área, suponiendo que corresponde a la figura roja principal.

También se estableció un área mínima de 800 píxeles. Este valor permite ignorar manchas pequeñas y falsas detecciones. Si el contorno supera dicha área, se calcula su rectángulo delimitador utilizando `cv2.boundingRect()`.

En la ejecución correspondiente al color rojo, el algoritmo dibuja un recuadro alrededor del rectángulo rojo de la imagen. El recuadro se dibuja sobre la imagen original a color, no sobre la máscara, lo que permite observar simultáneamente la escena capturada y el resultado del procesamiento.

### Sobre la identificación visual

Además del recuadro, el programa coloca el texto **“Rojo”** encima de la figura detectada. El texto utiliza el mismo color rojo del objeto para que la identificación sea clara.

El resultado esperado es que la imagen conserve sus colores originales y que únicamente la figura roja tenga:

- Un recuadro delimitador.
- La etiqueta “Rojo”.
- Una posición y tamaño calculados automáticamente a partir del contorno.

Las figuras verde y azul no reciben recuadros ni etiquetas durante esta ejecución, porque el programa está configurado para procesar un solo color a la vez.

### Sobre la ejecución individual por color

El programa fue organizado para que cada ejecución utilice un único color. Para la primera prueba, el color rojo queda seleccionado por defecto. Posteriormente, el mismo procedimiento puede repetirse utilizando los rangos HSV del verde y del azul.

Esta estrategia permite comprobar de manera independiente si cada color está correctamente segmentado. También facilita ajustar los rangos HSV de un color específico sin que las detecciones de los otros colores interfieran en el resultado.

### Factores que pueden afectar el resultado

El reconocimiento depende de las condiciones de iluminación y de la cámara. Una iluminación muy intensa puede producir reflejos blancos sobre la figura, reduciendo su saturación. Por otro lado, una iluminación insuficiente puede disminuir el valor de brillo y hacer que algunos píxeles queden fuera del rango definido.

También pueden presentarse dificultades si la cámara modifica automáticamente el balance de blancos o la exposición. Por esta razón, los valores HSV funcionan como una configuración inicial y podrían necesitar ajustes dependiendo del material utilizado, la cámara y el ambiente.

El parámetro `AREA_MINIMA` también influye en la detección. Si se utiliza un valor demasiado alto, una figura pequeña podría ser ignorada. Si se utiliza un valor demasiado bajo, podrían aparecer detecciones producidas por ruido.

### Conclusión general

Este reto permitió implementar un sistema básico de visión artificial capaz de segmentar y seguir una figura de color en una imagen o en un video. Para la primera ejecución, el algoritmo identifica el color rojo mediante rangos HSV, crea una máscara binaria, elimina ruido, encuentra el contorno principal y calcula automáticamente el bounding box de la figura.

El resultado se presenta sobre la imagen original mediante un recuadro y una etiqueta con el nombre del color detectado. La figura roja puede ser diferenciada del fondo blanco y de las figuras verde y azul porque sus píxeles cumplen las condiciones de tono, saturación y brillo establecidas.

El ejercicio demuestra que la segmentación por color no consiste únicamente en buscar valores RGB exactos, sino en definir rangos que toleren variaciones producidas por la iluminación y la cámara. Además, el uso de contornos permite transformar la máscara de color en información geométrica útil, como la posición, el ancho y la altura de la figura.

Finalmente, el mismo procedimiento puede repetirse de forma independiente para los colores verde y azul modificando el color seleccionado. De esta manera, se comprueba progresivamente la capacidad del sistema para reconocer cada figura y mostrar su clasificación directamente sobre el video.

## Ejecución

Para detectar el color rojo usando la cámara, ejecuta:

```powershell
C:/Users/juand/AppData/Local/Programs/Python/Python313/python.exe seguimiento_color.py --color rojo
```

El rojo es el color seleccionado por defecto, por lo que también puede ejecutarse simplemente con:

```powershell
C:/Users/juand/AppData/Local/Programs/Python/Python313/python.exe seguimiento_color.py
```

Durante la ejecución:

- Pulsa `q` para cerrar el programa.
- Pulsa `s` para guardar una captura de la detección.

Para las siguientes pruebas, se puede cambiar el color:

```powershell
C:/Users/juand/AppData/Local/Programs/Python/Python313/python.exe seguimiento_color.py --color verde
C:/Users/juand/AppData/Local/Programs/Python/Python313/python.exe seguimiento_color.py --color azul
```
