import sqlite3

from cli.persistence.database_handler import DatabaseHandler
from cli.persistence.template_models import (Template, Reference, Tag, Layer,
                                             CompleteTemplate)


class SQLiteDatabaseHandler(DatabaseHandler):
    _instance = None
    _DATABASE = "templates.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._connection: sqlite3.Connection | None = None
        self._initialized = True

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def connect(self) -> None:
        if self._connection is None:
            self._connection = sqlite3.connect(self._DATABASE)

    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    # ------------------------------------------------------------------
    # TemplateRepository
    # ------------------------------------------------------------------

    def create_template(self, template: Template) -> None:
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO Template (TemplateID, ReferenceID)
                VALUES (?, ?)
                """,
                (template.TemplateID, template.ReferenceID)
            )

    def get_template(self, template_id: str) -> Template | None:
        cursor = self._connection.execute(
            """
            SELECT TemplateID, ReferenceID
            FROM Template
            WHERE TemplateID = ?
            """,
            (template_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Template(
            TemplateID=row["TemplateID"],
            ReferenceID=row["ReferenceID"]
        )

    def delete_template(self, template_id: str) -> None:
        with self._connection:
            self._connection.execute(
                "DELETE FROM Template WHERE TemplateID = ?",
                (template_id,)
            )

    def get_by_reference(self, reference_id: int) -> list[Template]:
        cursor = self._connection.execute(
            """
            SELECT TemplateID, ReferenceID
            FROM Template
            WHERE ReferenceID = ?
            """,
            (reference_id,)
        )

        return [
            Template(
                TemplateID=row["TemplateID"],
                ReferenceID=row["ReferenceID"]
            )
            for row in cursor.fetchall()
        ]

    def get_complete(self, reference_id: int, tag: str
                     ) -> list[CompleteTemplate]:
        cursor = self._connection.execute(
            """
            SELECT
                t.TemplateID,
                r.ReferenceID,
                r.Description,
                r.Host,
                r.Port,
                r.Namespace,
                r.Repository,
                g.Tag
            FROM Template t
            JOIN Reference r
                ON t.ReferenceID = r.ReferenceID
            JOIN Tag g
                ON t.TemplateID = g.TemplateID
            WHERE
                t.ReferenceID = ?
                AND g.Tag = ?
            """,
            (reference_id, tag),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        template_id = row["TemplateID"]

        return CompleteTemplate(
            TemplateID=template_id,
            Reference=Reference(
                ReferenceID=row["ReferenceID"],
                Description=row["Description"],
                Host=row["Host"],
                Port=row["Port"],
                Namespace=row["Namespace"],
                Repository=row["Repository"],
            ),
            Tag=row["Tag"],
            Layers=self.get_layers(template_id),
        )

    # ------------------------------------------------------------------
    # ReferenceRepository
    # ------------------------------------------------------------------

    def create_reference(self, reference: Reference) -> None:
        self._connection.execute(
            """
            INSERT INTO Reference
            (ReferenceID, Description, Host, Port, Namespace, Repository)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                reference.ReferenceID,
                reference.Description,
                reference.Host,
                reference.Port,
                reference.Namespace,
                reference.Repository,
            ),
        )

    def get_reference(self, reference_id: int) -> Reference | None:
        cursor = self._connection.execute(
            """
            SELECT *
            FROM Reference
            WHERE ReferenceID = ?
            """,
            (reference_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Reference(
            ReferenceID=row["ReferenceID"],
            Description=row["Description"],
            Host=row["Host"],
            Port=row["Port"],
            Namespace=row["Namespace"],
            Repository=row["Repository"],
        )

    def delete_reference(self, reference_id: int) -> None:
        self._connection.execute(
            "DELETE FROM Reference WHERE ReferenceID = ?",
            (reference_id,),
        )

    # ------------------------------------------------------------------
    # TagRepository
    # ------------------------------------------------------------------

    def create_tag(self, tag: Tag) -> None:
        self._connection.execute(
            """
            INSERT INTO Tag (TemplateID, Tag)
            VALUES (?, ?)
            """,
            (tag.TemplateID, tag.Tag),
        )

    def get_by_template(self, template_id: str) -> list[Tag]:
        cursor = self._connection.execute(
            """
            SELECT TemplateID, Tag
            FROM Tag
            WHERE TemplateID = ?
            """,
            (template_id,),
        )

        return [
            Tag(
                TemplateID=row["TemplateID"],
                Tag=row["Tag"],
            )
            for row in cursor.fetchall()
        ]

    def delete_tag(self, template_id: str, tag: str) -> None:
        self._connection.execute(
            """
            DELETE FROM Tag
            WHERE TemplateID = ?
              AND Tag = ?
            """,
            (template_id, tag),
        )

    # ------------------------------------------------------------------
    # LayerRepository
    # ------------------------------------------------------------------

    def create_layer(self, layer: Layer) -> None:
        self._connection.execute(
            """
            INSERT INTO Layer
            (TemplateID, LayerID, LayerStep)
            VALUES (?, ?, ?)
            """,
            (
                layer.TemplateID,
                layer.LayerID,
                layer.LayerStep,
            ),
        )

    def get_layers(self, template_id: str) -> list[Layer]:
        cursor = self._connection.execute(
            """
            SELECT *
            FROM Layer
            WHERE TemplateID = ?
            ORDER BY LayerStep
            """,
            (template_id,),
        )

        return [
            Layer(
                TemplateID=row["TemplateID"],
                LayerID=row["LayerID"],
                LayerStep=row["LayerStep"],
            )
            for row in cursor.fetchall()
        ]

    def delete_layer(self, template_id: str, layer_id: str) -> None:
        self._connection.execute(
            """
            DELETE FROM Layer
            WHERE TemplateID = ?
            AND LayerID = ?
            """,
            (template_id, layer_id),
        )
