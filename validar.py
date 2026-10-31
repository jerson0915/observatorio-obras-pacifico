"""Revisa los datos antes de publicarlos. GitHub Actions lo corre después de los notebooks:
si encuentra un error, termina con código 1 y la actualización no se guarda ni se publica.

    python validar.py

Compara contra la versión guardada en git (HEAD) para detectar caídas bruscas."""
import io, os, subprocess, sys
import pandas as pd

FUENTES = ["SECOP I", "SECOP II"]
MUNICIPIOS = ["GUAPI", "TIMBIQUI", "LOPEZ DE MICAY"]
CAIDA_MAXIMA = 0.10        # error si hay más de 10 % menos contratos que la versión anterior
CAIDA_VALOR_AVISO = 0.20   # aviso si el valor total baja más de 20 %

errores, avisos, resumen = [], [], []


def anterior(ruta):
    """La versión de un archivo en el último commit, o None si no existe."""
    r = subprocess.run(["git", "show", f"HEAD:{ruta}"], capture_output=True)
    return pd.read_csv(io.BytesIO(r.stdout)) if r.returncode == 0 and r.stdout else None


obras = pd.read_csv("datos/obras_limpias.csv", parse_dates=["fecha_firma"])
resumen.append(f"Contratos: **{len(obras):,}** · valor **${obras['valor'].sum() / 1e9:,.1f} mil millones**")

if obras.empty:
    errores.append("La tabla de contratos quedó vacía.")

for fuente in FUENTES:
    n = (obras["fuente"] == fuente).sum()
    resumen.append(f"{fuente}: {n:,} contratos")
    if n == 0:
        errores.append(f"{fuente} no aportó ningún contrato: la fuente puede haber cambiado de columnas o estar caída.")

for municipio in MUNICIPIOS:
    if not (obras["municipio"] == municipio).any():
        errores.append(f"No hay contratos de {municipio}.")

if obras["valor"].isna().any():
    errores.append(f"{obras['valor'].isna().sum()} contratos sin valor.")
if (obras["valor"] < 0).any():
    errores.append(f"{(obras['valor'] < 0).sum()} contratos con valor negativo.")
if (obras["valor"] == 0).any():
    avisos.append(f"{(obras['valor'] == 0).sum()} contratos con valor 0.")
if obras["fecha_firma"].isna().any():
    errores.append(f"{obras['fecha_firma'].isna().sum()} contratos sin fecha de firma.")
if obras["id"].duplicated().any():
    errores.append(f"{obras['id'].duplicated().sum()} contratos repetidos (mismo id).")

previo = anterior("datos/obras_limpias.csv")
if previo is not None and len(previo):
    cambio = len(obras) / len(previo) - 1
    resumen.append(f"Frente a la versión anterior: {len(previo):,} → {len(obras):,} contratos ({cambio:+.1%})")
    if cambio < -CAIDA_MAXIMA:
        errores.append(f"El número de contratos cayó de {len(previo):,} a {len(obras):,} ({cambio:.0%}).")
    cambio_valor = obras["valor"].sum() / previo["valor"].sum() - 1
    if cambio_valor < -CAIDA_VALOR_AVISO:
        avisos.append(f"El valor total cayó {cambio_valor:.0%} frente a la versión anterior.")

if os.path.exists("datos/sin_contrato_limpio.csv"):
    sc = pd.read_csv("datos/sin_contrato_limpio.csv")
    resumen.append(f"Procesos adjudicados sin contrato: {len(sc):,}")
    if sc.empty:
        avisos.append("No llegó ningún proceso adjudicado sin contrato.")
    elif (sc["presupuesto"] < 0).any():
        errores.append("Hay procesos sin contrato con presupuesto negativo.")
else:
    errores.append("Falta datos/sin_contrato_limpio.csv.")

# Salida: en la consola y, en GitHub Actions, en el resumen de la ejecución y como anotaciones
lineas = ["## Validación de datos", *[f"- {r}" for r in resumen]]
lineas += [f"- ❌ {e}" for e in errores] + [f"- ⚠️ {a}" for a in avisos]
if not errores:
    lineas.append("- ✅ Todo en orden: se puede publicar.")
print("\n".join(lineas))
if os.environ.get("GITHUB_ACTIONS"):
    for e in errores:
        print(f"::error title=Datos::{e}")
    for a in avisos:
        print(f"::warning title=Datos::{a}")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
        f.write("\n".join(lineas) + "\n")
sys.exit(1 if errores else 0)
