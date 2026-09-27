"""Data Understanding sobre el corpus estructurado.

TODO(alumno): las visualizaciones no son decoración; deben revelar
cobertura, sesgos y problemas de calidad (nulos, JSON inválidos, nombres
inconsistentes).
"""
import pandas as pd
import matplotlib.pyplot as plt
import json 
from pathlib import Path

from src.excepciones import EtapaPendienteAlumno


class ExploradorDatos:
    """Estadísticas y gráficos mínimos del laboratorio."""
    def __init__(self):
        archivos = Path("data/json").glob("*.json")
        datos = []
        for archivo in archivos:
            with open(archivo, "r", encoding="utf-8") as f:
                datos.append(json.load(f))
        
        self.df = pd.DataFrame(datos)

    def noticias_por_fuente(self):
        if self.df.empty:
            return
            
        conteo = self.df['fuente'].value_counts()
        conteo.plot(kind='bar', color='blue', edgecolor='black')
        plt.title('Cantidad de Noticias por Fuente')
        plt.xlabel('Fuente')
        plt.ylabel('Cantidad de Noticias')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def delitos_frecuentes(self):
        if 'delitos' not in self.df.columns:
            return
            
        df_delitos = self.df.explode('delitos')
        conteo = df_delitos['delitos'].value_counts().head(10) # Top 10 delitos
        
        conteo.plot(kind='bar', color='orange', edgecolor='black')
        plt.title('Top 10 Delitos Más Frecuentes')
        plt.xlabel('Tipo de Delito')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def lugares_frecuentes(self):
        if 'lugares' not in self.df.columns:
            return
            
        df_lugares = self.df.explode('lugares')
        conteo = df_lugares['lugares'].value_counts().head(10)
        
        conteo.plot(kind='bar', color='green', edgecolor='black')
        plt.title('Top 10 Lugares con Mayor Mención')
        plt.xlabel('Lugar (Comuna/Región)')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def campos_faltantes(self):
        if self.df.empty:
            return
        nulos = self.df.map(lambda x: x is None or x == [] or (isinstance(x, float) and pd.isna(x))).mean() * 100
        nulos.plot(kind='bar', color='red', edgecolor='black')
        plt.title('Porcentaje de Campos Faltantes por Atributo')
        plt.xlabel("Campos")
        plt.ylabel("Porcentaje de faltantes")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        

    def evolucion_temporal(self):
        if 'fecha_publicacion' not in self.df.columns:
            return
        conteo = self.df['fecha_publicacion'].value_counts().sort_index()
        conteo.plot(kind='line', marker='o', color = 'blue')
        plt.title('Evolución temporal de noticias')
        plt.xlabel('Fecha de publicación')
        plt.ylabel('Cantidad de noticias')
        plt.xticks(rotation=45)
        plt.grid(True,linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def ejecutar(self):
        """Corre todas las visualizaciones pedidas en la guía."""
        print("Iniciando Análisis exploratorio de datos...")
        if self.df.empty:
            print("No hay datos para analizar. Verificar la extracción JSON.")
            return

        self.noticias_por_fuente()
        self.delitos_frecuentes()
        self.lugares_frecuentes()
        self.campos_faltantes()
        self.evolucion_temporal()