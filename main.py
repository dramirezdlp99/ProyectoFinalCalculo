import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sp.init_printing()

def parse_function(input_str):
    return sp.sympify(input_str.replace('^', '**'))

def identificar_superficie_cuadrica(func_expr, variables):
    """Identifica si la función corresponde a una superficie cuádrica conocida."""
    if len(variables) != 3:
        return None
    
    x, y, z = variables
    expr = sp.expand(func_expr)
    
    # Patrones para reconocer superficies cuádricas
    try:
        # Elipsoide: x²/a² + y²/b² + z²/c² = 1
        if expr.is_Add and len(expr.args) == 3:
            terms = [term for term in expr.args if term.is_Mul or term.is_Pow]
            if all(term.has(x**2) for term in terms) or all(term.has(y**2) for term in terms) or all(term.has(z**2) for term in terms):
                return "Elipsoide"
        
        # Hiperboloide de una hoja: x²/a² + y²/b² - z²/c² = 1
        # Hiperboloide de dos hojas: -x²/a² - y²/b² + z²/c² = 1
        if expr.is_Add:
            pos = [term for term in expr.args if (term.coeff(x**2) > 0 if term.has(x**2) else False) or 
                                           (term.coeff(y**2) > 0 if term.has(y**2) else False) or 
                                           (term.coeff(z**2) > 0 if term.has(z**2) else False)]
            neg = [term for term in expr.args if (term.coeff(x**2) < 0 if term.has(x**2) else False) or 
                                           (term.coeff(y**2) < 0 if term.has(y**2) else False) or 
                                           (term.coeff(z**2) < 0 if term.has(z**2) else False)]
            if len(pos) == 2 and len(neg) == 1:
                return "Hiperboloide de una hoja"
            elif len(pos) == 1 and len(neg) == 2:
                return "Hiperboloide de dos hojas"
        
        # Paraboloide elíptico: z/c = x²/a² + y²/b²
        # Paraboloide hiperbólico: z/c = x²/a² - y²/b²
        if expr.is_Add and len(expr.args) == 2:
            z_terms = [term for term in expr.args if term.has(z) and not (term.has(x**2) or term.has(y**2))]
            if z_terms:
                other_terms = [term for term in expr.args if term not in z_terms]
                if len(other_terms) == 2:
                    x2_coeff = other_terms[0].coeff(x**2) if other_terms[0].has(x**2) else 0
                    y2_coeff = other_terms[0].coeff(y**2) if other_terms[0].has(y**2) else 0
                    if x2_coeff > 0 and y2_coeff > 0:
                        return "Paraboloide elíptico"
                    elif (x2_coeff > 0 and y2_coeff < 0) or (x2_coeff < 0 and y2_coeff > 0):
                        return "Paraboloide hiperbólico"
        
        # Cono elíptico: x²/a² + y²/b² = z²/c²
        if expr.is_Add and len(expr.args) == 2:
            if (all(term.has(x**2) or term.has(y**2) for term in expr.args) or 
                all(term.has(z**2) for term in expr.args)):
                return "Cono elíptico"
        
        # Cilindros
        if not any(term.has(z) for term in expr.args):
            if any(term.has(x**2) for term in expr.args) and any(term.has(y**2) for term in expr.args):
                return "Cilindro elíptico"
            elif (any(term.has(x**2) for term in expr.args) and not any(term.has(y**2) for term in expr.args)) or \
                 (not any(term.has(x**2) for term in expr.args) and any(term.has(y**2) for term in expr.args)):
                return "Cilindro parabólico"
    
    except Exception as e:
        print(f"Error al identificar superficie cuádrica: {e}")
        return None
    
    return None

def graficar_funcion_2d(fx, var):
    nombre_funcion = f"f({var}) = {fx}"
    sp.plot(fx, (var, -10, 10), title=nombre_funcion, xlabel=str(var), ylabel=f'f({var})', show=True)

def graficar_funcion_3d_cuadrica(fxy, x, y, z):
    """Función especial para graficar superficies cuádricas"""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    X_vals = np.linspace(-5, 5, 100)
    Y_vals = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(X_vals, Y_vals)
    
    # Resolver para z
    soluciones = sp.solve(fxy, z)
    if not soluciones:
        print("❌ No se pudo resolver para z la ecuación")
        return
    
    for sol in soluciones:
        f_lambdified = sp.lambdify((x, y), sol, modules='numpy')
        try:
            Z = f_lambdified(X, Y)
            superficie = identificar_superficie_cuadrica(fxy, [x, y, z])
            titulo = f"Superficie: {superficie}\n{fxy} = 0" if superficie else f"{fxy} = 0"
            
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
            ax.set_title(titulo, pad=20)
            ax.set_xlabel(str(x))
            ax.set_ylabel(str(y))
            ax.set_zlabel(str(z))
            plt.tight_layout()
        except Exception as e:
            print(f"❌ Error al graficar solución {sol}: {e}")
    
    plt.show()

def graficar_funcion_3d(fxy, x, y):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    X_vals = np.linspace(-5, 5, 100)
    Y_vals = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(X_vals, Y_vals)
    
    f_lambdified = sp.lambdify((x, y), fxy, modules='numpy')
    
    try:
        Z = f_lambdified(X, Y)
        
        # Identificar si es una superficie cuádrica
        variables = sorted(fxy.free_symbols, key=lambda v: str(v))
        if len(variables) == 3:
            z = [var for var in variables if var not in (x, y)][0]
            superficie = identificar_superficie_cuadrica(fxy - z, variables)
            titulo = f"Superficie: {superficie}\n{z} = {fxy}" if superficie else f"f({x},{y}) = {fxy}"
        else:
            titulo = f"f({x},{y}) = {fxy}"
        
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
        ax.set_title(titulo, pad=20)
        ax.set_xlabel(str(x))
        ax.set_ylabel(str(y))
        ax.set_zlabel('z')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"❌ Error al graficar: {e}")

def calcular_derivadas(func_expr, variables):
    derivadas = {}
    print("\n📘 Derivadas parciales:")
    for var in variables:
        d = sp.diff(func_expr, var)
        derivadas[var] = d
        print(f"∂f/∂{var} = {sp.simplify(d)}")
    return derivadas

def encontrar_puntos_criticos(func_expr, variables):
    print("\n📘 Buscando puntos críticos...")
    grad = [sp.diff(func_expr, var) for var in variables]
    sistema = [sp.Eq(g, 0) for g in grad]
    criticos = sp.solve(sistema, variables, dict=True)
    if criticos:
        print("✅ Puntos críticos encontrados:")
        for punto in criticos:
            print({k: sp.simplify(v) for k, v in punto.items()})
    else:
        print("⚠️ No se encontraron puntos críticos.")
    return criticos

def calcular_integral(func_expr, variables):
    if len(variables) == 1:
        a_str = input(f"🔢 Límite inferior para {variables[0]}: ")
        b_str = input(f"🔢 Límite superior para {variables[0]}: ")
        try:
            a = sp.sympify(a_str)
            b = sp.sympify(b_str)
            resultado = sp.integrate(func_expr, (variables[0], a, b))
            print(f"\n📘 Integral definida: ∫ f({variables[0]}) d{variables[0]} de {a} a {b} = {sp.simplify(resultado)}")
        except Exception as e:
            print(f"❌ Error al calcular la integral: {e}")
    elif len(variables) == 2:
        x, y = variables
        ax_str = input("🔢 Límite inferior para x: ")
        bx_str = input("🔢 Límite superior para x: ")
        ay_str = input("🔢 Límite inferior para y: ")
        by_str = input("🔢 Límite superior para y: ")
        try:
            ax = sp.sympify(ax_str)
            bx = sp.sympify(bx_str)
            ay = sp.sympify(ay_str)
            by = sp.sympify(by_str)
            resultado = sp.integrate(sp.integrate(func_expr, (x, ax, bx)), (y, ay, by))
            print(f"\n📘 Integral doble definida sobre región [{ax},{bx}] x [{ay},{by}] = {sp.simplify(resultado)}")
        except Exception as e:
            print(f"❌ Error al calcular la integral: {e}")
    elif len(variables) == 3:
        x, y, z = variables
        ax_str = input("🔢 Límite inferior para x: ")
        bx_str = input("🔢 Límite superior para x: ")
        ay_str = input("🔢 Límite inferior para y: ")
        by_str = input("🔢 Límite superior para y: ")
        az_str = input("🔢 Límite inferior para z: ")
        bz_str = input("🔢 Límite superior para z: ")
        try:
            ax = sp.sympify(ax_str)
            bx = sp.sympify(bx_str)
            ay = sp.sympify(ay_str)
            by = sp.sympify(by_str)
            az = sp.sympify(az_str)
            bz = sp.sympify(bz_str)
            resultado = sp.integrate(sp.integrate(sp.integrate(func_expr, (x, ax, bx)), (y, ay, by)), (z, az, bz))
            print(f"\n📘 Integral triple definida sobre región [{ax},{bx}] x [{ay},{by}] x [{az},{bz}] = {sp.simplify(resultado)}")
        except Exception as e:
            print(f"❌ Error al calcular la integral: {e}")
    else:
        print("⚠️ Solo se admite hasta 3 variables para integración.")

def optimizacion_lagrange():
    print("\n🔍 Optimización con Restricciones (Multiplicadores de Lagrange)")
    f_str = input("✍️ Ingrese la función objetivo f(x,y,z): ")
    g_str = input("✍️ Ingrese la restricción g(x,y,z) = 0: ")
    
    try:
        f = parse_function(f_str)
        g = parse_function(g_str)
        variables = sorted(list(f.free_symbols | g.free_symbols), key=lambda x: str(x))
        
        if len(variables) < 2 or len(variables) > 3:
            print("⚠️ Solo se admiten 2 o 3 variables")
            return
            
        lambda_ = sp.symbols('λ')
        L = f - lambda_ * g
        
        ecuaciones = [sp.diff(L, var) for var in variables] + [g]
        soluciones = sp.solve(ecuaciones, variables + [lambda_], dict=True)
        
        if soluciones:
            print("\n✅ Puntos críticos encontrados:")
            for i, sol in enumerate(soluciones, 1):
                print(f"\nSolución {i}:")
                for var in variables:
                    print(f"{var} = {sp.simplify(sol[var])}")
                print(f"λ = {sp.simplify(sol[lambda_])}")
                print(f"Valor de f: {f.subs(sol).simplify()}")
        else:
            print("⚠️ No se encontraron puntos críticos que satisfagan las condiciones")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    while True:
        print("\n🧮 Menú Principal")
        print("1. Derivar función y encontrar puntos críticos")
        print("2. Calcular integral definida")
        print("3. Graficar función")
        print("4. Optimización con restricciones (Lagrange)")
        print("5. Salir")

        opcion = input("➡️ Selecciona una opción: ")

        if opcion not in ['1', '2', '3', '4', '5']:
            print("❌ Opción no válida. Intenta de nuevo.")
            continue

        if opcion == '5':
            print("👋 Saliendo del programa...")
            break
            
        if opcion == '4':
            optimizacion_lagrange()
            continue

        entrada_funcion = input("✍️ Ingrese la función (ej: x^2 + y^2 o sin(x*y^2)): ")
        try:
            funcion = parse_function(entrada_funcion)
        except Exception as e:
            print(f"❌ Error al interpretar la función: {e}")
            continue

        variables = sorted(funcion.free_symbols, key=lambda v: str(v))

        if not variables:
            print("⚠️ La función no contiene variables.")
            continue

        print(f"🔎 Variables detectadas: {variables}")

        if opcion == '1':
            derivadas = calcular_derivadas(funcion, variables)
            encontrar_puntos_criticos(funcion, variables)

        elif opcion == '2':
            calcular_integral(funcion, variables)

        elif opcion == '3':
            if len(variables) == 1:
                graficar_funcion_2d(funcion, variables[0])
            elif len(variables) == 2:
                graficar_funcion_3d(funcion, variables[0], variables[1])
            elif len(variables) == 3:
                z = variables[-1]
                graficar_funcion_3d_cuadrica(funcion, variables[0], variables[1], z)
            else:
                print("⚠️ Para graficar, se admiten hasta 3 variables")

if __name__ == "__main__":
    main()