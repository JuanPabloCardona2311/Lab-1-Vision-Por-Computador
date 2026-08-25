import argparse

import cv2  # pyright: ignore[reportMissingImports]
import numpy as np


AREA_MINIMA = 800

colores = {
    "rojo": {
        "nombre": "Rojo",
        "bajo1": np.array([0, 120, 70]),
        "alto1": np.array([10, 255, 255]),
        "bajo2": np.array([170, 120, 70]),
        "alto2": np.array([180, 255, 255]),
        "bgr": (0, 0, 255),
    },
    "verde": {
        "nombre": "Verde",
        "bajo1": np.array([40, 70, 70]),
        "alto1": np.array([80, 255, 255]),
        "bgr": (0, 255, 0),
    },
    "azul": {
        "nombre": "Azul",
        "bajo1": np.array([100, 100, 70]),
        "alto1": np.array([130, 255, 255]),
        "bgr": (255, 0, 0),
    },
}


def crear_mascara(hsv, datos):
    mascara = cv2.inRange(hsv, datos["bajo1"], datos["alto1"])

    if "bajo2" in datos:
        mascara2 = cv2.inRange(hsv, datos["bajo2"], datos["alto2"])
        mascara = cv2.bitwise_or(mascara, mascara2)

    kernel = np.ones((5, 5), np.uint8)
    mascara = cv2.erode(mascara, kernel, iterations=1)
    mascara = cv2.dilate(mascara, kernel, iterations=2)
    return mascara


def dibujar_deteccion(frame, mascara, datos):
    contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contornos:
        return frame

    contorno_mayor = max(contornos, key=cv2.contourArea)
    area = cv2.contourArea(contorno_mayor)

    if area < AREA_MINIMA:
        return frame

    x, y, w, h = cv2.boundingRect(contorno_mayor)
    cv2.rectangle(frame, (x, y), (x + w, y + h), datos["bgr"], 2)
    cv2.putText(
        frame,
        datos["nombre"],
        (x, max(25, y - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        datos["bgr"],
        2,
    )
    return frame


def procesar_frame(frame, color_clave):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    datos = colores[color_clave]
    mascara = crear_mascara(hsv, datos)
    return dibujar_deteccion(frame, mascara, datos)


def ejecutar_con_camara(color_clave):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: no se pudo acceder a la camara. Revisa permisos o si otra app la esta usando.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ERROR: no se pudo leer el frame de la camara.")
            break

        frame = procesar_frame(frame, color_clave)
        cv2.imshow("Seguimiento de figura por color", frame)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord("q"):
            break
        if tecla == ord("s"):
            cv2.imwrite("captura_deteccion.png", frame)
            print("Captura guardada como captura_deteccion.png")

    cap.release()
    cv2.destroyAllWindows()


def ejecutar_con_imagen(ruta_imagen, color_clave):
    frame = cv2.imread(ruta_imagen)

    if frame is None:
        print(f"ERROR: no se pudo abrir la imagen: {ruta_imagen}")
        return

    frame = procesar_frame(frame, color_clave)
    cv2.imshow("Seguimiento de figura por color", frame)
    print("Pulsa una tecla para cerrar la ventana.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="Seguimiento de figura por color")
    parser.add_argument(
        "--color",
        default="azul",
        choices=["rojo", "verde", "azul"],
        help="Color a detectar en esta ejecucion.",
    )
    parser.add_argument(
        "--image",
        default=None,
        help="Ruta de una imagen para probar la deteccion sin usar la camara.",
    )
    args = parser.parse_args()

    if args.image:
        ejecutar_con_imagen(args.image, args.color)
    else:
        ejecutar_con_camara(args.color)


if __name__ == "__main__":
    main()