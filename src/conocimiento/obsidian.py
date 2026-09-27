"""Persistencia final: red de notas Markdown para Obsidian.

No se usa SQLite, MongoDB ni Neo4j. Cada noticia y cada entidad debe
tener su propia nota, enlazada con [[wiki-links]].
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import os
from pathlib import Path
from collections import defaultdict
from src.conocimiento.utilidades import slugify

from src.config import DIR_VAULT
from src.excepciones import EtapaPendienteAlumno

class EscritorObsidian(ABC):
    """Contrato para generar la bóveda a partir de JSON validado."""

    @abstractmethod
    def escribir_noticia(self, data: dict) -> Path:
        """Crea obsidian_vault/Noticias/{id_noticia}.md con frontmatter y enlaces."""
        delitos_md = "\n".join([f"- [[{slugify(d)}]]" for d in data.get("delitos", [])])
        lugares_md = "\n".join([f"- [[{slugify(l)}]]" for l in data.get("lugares", [])])

        personas_md = "\n".join([f"- [[{slugify(p['nombre'])}]] ({p.get('rol', '')})" for p in data.get("personas", []) if isinstance(p, dict)])

        plantilla = f"""---
        id: {data.get('id_noticia')}
        fecha_publicacion: {data.get('fecha_publicacion')}
        fuente: {data.get('fuente')}
        url: {data.get('url')}
        ---
        # {data.get('titulo')}

        ## Resumen
        {data.get('resumen')}

        ## Delitos
        {delitos_md}

        ## Personas
        {personas_md}

        ## Lugares
        {lugares_md}
        """

        ruta = Path(f"obsidian_vault/Noticias/{data['id_noticia']}.md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(plantilla)

        return ruta

    @abstractmethod
    def escribir_entidades(self, noticias: list[dict]) -> None:
        """Agrega notas de delitos, personas, organizaciones, lugares y objetos."""

        indice_delitos = defaultdict(set)
        indice_lugares = defaultdict(set)

        for data in noticias:
            nid = data.get("id_noticia")
            
            for delito in data.get("delitos", []):
                indice_delitos[slugify(delito)].add(nid)
                
            for lugar in data.get("lugares", []):
                indice_lugares[slugify(lugar)].add(nid)

        for delito, ids_noticias in indice_delitos.items():
            ruta_delito = Path(f"obsidian_vault/Delitos/{delito}.md")
            enlace_noticia = "\n".join([f"- [[Noticias/{nid}]]" for nid in ids_noticias])
            plantilla = f"# {delito}\n\nTipo: Delito\n\n## Noticias relacionadas:\n{enlace_noticia}\n"
            with open(ruta_delito, "w", encoding="utf-8") as f:
                f.write(plantilla)

        for lugar, ids_noticias in indice_lugares.items():
            ruta_lugar = Path(f"obsidian_vault/Lugares/{lugar}.md")
            enlace_noticia = "\n".join([f"- [[Noticias/{nid}]]" for nid in ids_noticias])
            plantilla = f"# {lugar}\n\nTipo: Lugar\n\n## Noticias relacionadas:\n{enlace_noticia}\n"
            with open(ruta_lugar, "w", encoding="utf-8") as f:
                f.write(plantilla)

    @abstractmethod
    def escribir_indice(self, noticias: list[dict]) -> Path:
        """Crea obsidian_vault/00_Indice.md."""
        ruta =  Path("obsidian_vault/00_Indice.md")
        enlaces_noticias = "\n".join([f"- [[{data.get('id_noticia')}]] - {data.get('titulo')}" for data in noticias])
        plantilla = f"""# Índice de Noticias Delictivas
        ##Registro de Noticias
        {enlaces_noticias}
        """
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(plantilla)
        return ruta

    @abstractmethod
    def escribir_vault(self, noticias: list[dict]) -> None:
        """Orquesta noticia + entidades + índice."""
        print("Iniciando generacion de Obsidian Vault...")
        for data in noticias:
            self.escribir_noticia(data)
        self.escribir_entidades(noticias)
        self.escribir_indice(noticias)
        print("Vault de Obsidian generado exitosamente")

        


class EscritorVaultObsidian(EscritorObsidian):
    """Implementación objetivo del laboratorio.

    Use src.conocimiento.utilidades.slugify y enlace_obsidian.
    Jerarquía esperada:
        obsidian_vault/
        ├── 00_Indice.md
        ├── Noticias/
        ├── Delitos/
        ├── Personas/
        ├── Organizaciones/
        ├── Lugares/
        ├── Objetos/
        └── Relaciones/
    """

    def __init__(self, vault: Path = DIR_VAULT) -> None:
        self.vault = vault

    def escribir_noticia(self, data: dict) -> Path:
        # TODO(alumno): plantilla Markdown con YAML, resumen y [[enlaces]].

        raise EtapaPendienteAlumno(
            modulo="src.conocimiento.obsidian.EscritorVaultObsidian.escribir_noticia",
            pista="Genere Noticias/{id}.md con delitos, personas, lugares y relaciones enlazadas.",
        )

    def escribir_entidades(self, noticias: list[dict]) -> None:
        # TODO(alumno): índices con defaultdict(set) agrupando por entidad.
        raise EtapaPendienteAlumno(
            modulo="src.conocimiento.obsidian.EscritorVaultObsidian.escribir_entidades",
            pista="Una nota por delito/persona/lugar con la lista de noticias relacionadas.",
        )

    def escribir_indice(self, noticias: list[dict]) -> Path:
        # TODO(alumno): índice navegable de toda la bóveda.
        raise EtapaPendienteAlumno(
            modulo="src.conocimiento.obsidian.EscritorVaultObsidian.escribir_indice",
            pista="Escriba 00_Indice.md listando noticias y entidades.",
        )

    def escribir_vault(self, noticias: list[dict]) -> None:
        # TODO(alumno): llamar a los tres métodos anteriores en orden.
        raise EtapaPendienteAlumno(
            modulo="src.conocimiento.obsidian.EscritorVaultObsidian.escribir_vault",
            pista="Recorra data/json/*.json, valide y escriba la jerarquía completa del vault.",
        )
