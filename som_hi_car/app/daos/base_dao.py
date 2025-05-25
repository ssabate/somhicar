# app/daos/base_dao.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

T = TypeVar('T')  # Variable de tipus per a l'entitat

class BaseDAO(Generic[T], ABC):
    def __init__(self, db):
        """
        Inicialitza el DAO amb una connexió a la base de dades (SQLAlchemy).
        :param db: Objecte SQLAlchemy (p. ex., db de database.db).
        """
        self.db = db

    @abstractmethod
    def get_all(self) -> List[T]:
        """Retorna totes les entitats."""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T:
        """Retorna una entitat per ID."""
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        """Afegeix una nova entitat."""
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        """Actualitza una entitat existent."""
        pass

    @abstractmethod
    def delete(self, entity: T) -> None:
        """Elimina una entitat."""
        pass

    def _validate_entity(self, entity: T) -> bool:
        """
        Valida l'entitat abans de guardar-la o actualitzar-la.
        :param entity: Objecte a validar.
        :return: True si és vàlid, False altrament.
        """
        return True