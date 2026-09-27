"""Persistencia final: red de notas Markdown para Obsidian.

No se usa SQLite, MongoDB ni Neo4j. Cada noticia y cada entidad debe
tener su propia nota, enlazada con [[wiki-links]].
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from collections import defaultdict
from src.conocimiento.utilidades import slugify

from src.config import DIR_VAULT
from src.excepciones import EtapaPendienteAlumno


class EscritorObsidian(ABC):
    """contrato para generar la bóveda a partir de JSON validado"""

    @abstractmethod
    def escribir_noticia(self, data: dict) -> Path:
        """crea obsidian_vault/Noticias/{id_noticia}.md con frontmatter y enlaces"""
        pass

    @abstractmethod
    def escribir_entidades(self, noticias: list[dict]) -> None:
        """agrega notas de delitos, personas, organizaciones, lugares y objetos"""
        pass

    @abstractmethod
    def escribir_indice(self, noticias: list[dict]) -> Path:
        """crea obsidian_vault/00_Indice.md"""
        pass

    @abstractmethod
    def escribir_vault(self, noticias: list[dict]) -> None:
        """orquesta noticia + entidades + índice"""
        pass


class EscritorVaultObsidian(EscritorObsidian):
    """implementación objetivo del laboratorio"""

    def __init__(self, vault: Path = DIR_VAULT) -> None:
        self.vault = vault

    def escribir_noticia(self, data: dict) -> Path:
        entidades = data.get("entidades", data)
        
        delitos_md = "\n".join([f"- [[{slugify(d)}]]" for d in entidades.get("delitos", [])])
        lugares_md = "\n".join([f"- [[{slugify(l)}]]" for l in entidades.get("lugares", [])])
        personas_md = "\n".join([f"- [[{slugify(p)}]]" for p in entidades.get("personas", [])])
        organizaciones_md = "\n".join([f"- [[{slugify(o)}]]" for o in entidades.get("organizaciones", [])])
        objetos_md = "\n".join([f"- [[{slugify(obj)}]]" for obj in entidades.get("objetos", [])])

        plantilla = f"""---
id: {data.get('id_noticia')}
fecha_publicacion: {data.get('fecha_publicacion', 'Desconocida')}
fuente: {data.get('fuente', 'Desconocida')}
url: {data.get('url', 'Desconocida')}
---
# {data.get('titulo', 'Sin titulo')}

## Resumen
{data.get('resumen', 'Sin resumen')}

## Delitos
{delitos_md}

## Personas
{personas_md}

## Organizaciones
{organizaciones_md}

## Lugares
{lugares_md}

## Objetos
{objetos_md}
"""
        ruta = self.vault / "Noticias" / f"{data['id_noticia']}.md"
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(plantilla)

        return ruta

    def escribir_entidades(self, noticias: list[dict]) -> None:
        indice_delitos = defaultdict(set)
        indice_lugares = defaultdict(set)
        indice_personas = defaultdict(set)
        indice_organizaciones = defaultdict(set)
        indice_objetos = defaultdict(set)

        for data in noticias:
            nid = data.get("id_noticia")
            entidades = data.get("entidades", data)
            
            for delito in entidades.get("delitos", []):
                indice_delitos[slugify(delito)].add(nid)
                
            for lugar in entidades.get("lugares", []):
                indice_lugares[slugify(lugar)].add(nid)
                
            for persona in entidades.get("personas", []):
                indice_personas[slugify(persona)].add(nid)
                
            for organizacion in entidades.get("organizaciones", []):
                indice_organizaciones[slugify(organizacion)].add(nid)
                
            for objeto in entidades.get("objetos", []):
                indice_objetos[slugify(objeto)].add(nid)

        for delito, ids_noticias in indice_delitos.items():
            if not delito: continue
            ruta_delito = self.vault / "Delitos" / f"{delito}.md"
            enlace_noticia = "\n".join([f"- [[{nid}]]" for nid in ids_noticias])
            plantilla = f"# {delito}\n\nTipo: Delito\n\n## Noticias relacionadas:\n{enlace_noticia}\n"
            with open(ruta_delito, "w", encoding="utf-8") as f:
                f.write(plantilla)

        for lugar, ids_noticias in indice_lugares.items():
            if not lugar: continue
            ruta_lugar = self.vault / "Lugares" / f"{lugar}.md"
            enlace_noticia = "\n".join([f"- [[{nid}]]" for nid in ids_noticias])
            plantilla = f"# {lugar}\n\nTipo: Lugar\n\n## Noticias relacionadas:\n{enlace_noticia}\n"
            with open(ruta_lugar, "w", encoding="utf-8") as f:
                f.write(plantilla)

        for persona, ids_noticias in indice_personas.items():
            if not persona: continue
            ruta_persona = self.vault / "Personas" / f"{persona}.md"
            enlace_noticia = "\n".join([f"- [[{nid}]]" for nid in ids_noticias])
            plantilla = f"# {persona}\n\nTipo: Persona\n\n## Noticias relacionadas:\n{enlace_noticia}\n"
            with open(ruta_persona, "w", encoding="utf-8") as f:
                f.write(plantilla)

        for organizacion, ids_noticias in indice_organizaciones.items():
            if not organizacion: continue
            ruta_organizacion = self.vault / "Organizaciones" / f"{organizacion}.md"
            enlace_noticia = "\n".join([f"- [[{nid}]]" for nid in ids_noticias])
            plantilla = f"# {organizacion}\n\nTipo: Organizacion\n\n## Noticias relacionadas:\n{enlace_noticia}\n"
            with open(ruta_organizacion, "w", encoding="utf-8") as f:
                f.write(plantilla)

        for objeto, ids_noticias in indice_objetos.items():
            if not objeto: continue
            ruta_objeto = self.vault / "Objetos" / f"{objeto}.md"
            enlace_noticia = "\n".join([f"- [[{nid}]]" for nid in ids_noticias])
            plantilla = f"# {objeto}\n\nTipo: Objeto\n\n## Noticias relacionadas:\n{enlace_noticia}\n"
            with open(ruta_objeto, "w", encoding="utf-8") as f:
                f.write(plantilla)

    def escribir_indice(self, noticias: list[dict]) -> Path:
        ruta = self.vault / "00_Indice.md"
        enlaces_noticias = "\n".join([f"- [[{data.get('id_noticia')}]] - {data.get('titulo')}" for data in noticias])
        plantilla = f"""# Índice de Noticias Delictivas

## Registro de Noticias
{enlaces_noticias}
"""
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(plantilla)
        return ruta

    def escribir_vault(self, noticias: list[dict]) -> None:
        print("Iniciando generacion de Obsidian Vault")
        
        carpetas = ["Noticias", "Delitos", "Personas", "Organizaciones", "Lugares", "Objetos", "Relaciones"]
        for c in carpetas:
            (self.vault / c).mkdir(parents=True, exist_ok=True)
            
        for data in noticias:
            self.escribir_noticia(data)
            
        self.escribir_entidades(noticias)
        self.escribir_indice(noticias)
        
        print("Vault de Obsidian generado exitosamente")