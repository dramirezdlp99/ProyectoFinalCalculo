# Aplicativo Interactivo de Cálculo Multivariado

Este proyecto consiste en el desarrollo de un aplicativo interactivo en consola, diseñado para apoyar el aprendizaje y la práctica de temas fundamentales del **Cálculo Multivariado**, tales como derivadas parciales, integrales múltiples, optimización con restricciones y visualización de superficies.

## 🎯 Objetivo del Proyecto

Diseñar y desarrollar un aplicativo interactivo que permita visualizar, calcular y/o interpretar conceptos de derivadas parciales o integrales múltiples.

## ✅ Requisitos Generales

### 1. Tipo de Aplicativo
- Aplicación funcional de **consola**, desarrollada en **Python**.

### 2. Enfoque Matemático
El aplicativo aborda múltiples temáticas del cálculo multivariado:
- Derivadas parciales y gradientes.
- Integración doble y triple.
- Optimización con restricciones usando multiplicadores de Lagrange.
- Visualización gráfica de funciones multivariables y superficies cuádricas.

### 3. Funcionalidades Mínimas
✔️ Ingreso dinámico de funciones multivariables.  
✔️ Cálculo automático de derivadas parciales y puntos críticos.  
✔️ Cálculo de integrales dobles con límites definidos por el usuario.  
✔️ Aplicación del método de **multiplicadores de Lagrange** para optimización con restricciones.  
✔️ Visualización 3D de funciones y superficies cuádricas.  
✔️ Interfaz de consola clara, organizada y fácil de usar.  

## 🧮 ¿Qué hace el programa?

Al ejecutar el programa, el usuario puede seleccionar entre las siguientes opciones del menú:

### 1. Derivar función y encontrar puntos críticos
- El usuario ingresa una función multivariable (ej: `x**2 + y**2`, `sin(x*y)`).
- El programa calcula las derivadas parciales.
- Determina los puntos críticos y su tipo (mínimo, máximo o punto silla).

### 2. Calcular integral definida
- Solicita una función y los límites de integración en `x` y `y`.
- Realiza la **integración doble** y devuelve el resultado.
- Útil para cálculos de volumen bajo superficies.

### 3. Graficar función
- Solicita una función de dos variables.
- Muestra su gráfico 3D para ayudar a visualizar su comportamiento.

### 4. Optimización con restricciones (Método de Lagrange)
- Solicita función objetivo y una restricción.
- Aplica el método de los multiplicadores de Lagrange.
- Devuelve los puntos que maximizan o minimizan la función bajo esa condición.

### 5. Salir
- Cierra el programa.

## 🛠️ Requisitos del sistema

### Archivos necesarios:
- `main.py` (archivo principal del programa).
- `requirements.txt` (lista de dependencias para instalar).

### Instalación de dependencias:

```bash
pip install -r requirements.txt
```

Dependencias utilizadas:
- `sympy` (álgebra simbólica).
- `numpy` (operaciones numéricas).
- `matplotlib` (visualización de funciones).

## 📘 Ejecución del programa

Para correr el programa:

```bash
python main.py
```

Sigue el menú interactivo para usar cada funcionalidad.

## 👥 Integrantes

- David Fernando Ramírez de la Parra  
- Daniers Alexander Solarte Limas  
- Juan Felipe Mora Revelo

## 🏫 Universidad

**Universidad Cooperativa de Colombia**  
**Materia:** Cálculo Multivariado, Cuarto semestre  
**Profesor:** Juan Pablo Granja Hinestrosa