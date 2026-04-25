"""Conexiones de infraestructura para MongoDB y Cassandra.

Este script centraliza la configuración de conexiones usando variables de entorno
con defaults locales adecuados para desarrollo.
"""

from __future__ import annotations

import os
from typing import Optional, Tuple

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from pymongo import MongoClient
from pymongo.errors import PyMongoError


# ------------------------------
# Configuración por environment
# ------------------------------
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_DB = os.getenv("MONGO_DB", "online_learning_platform")
MONGO_USER = os.getenv("MONGO_USER", "")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "")

CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "online_learning_platform")
CASSANDRA_USER = os.getenv("CASSANDRA_USER", "")
CASSANDRA_PASSWORD = os.getenv("CASSANDRA_PASSWORD", "")


def connect_mongo() -> Optional[MongoClient]:
    """Conecta a MongoDB y valida conexión con ping.

    Returns:
        MongoClient o None si falla.
    """
    try:
        if MONGO_USER and MONGO_PASSWORD:
            uri = (
                f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}"
                f"@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
            )
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        else:
            client = MongoClient(MONGO_HOST, MONGO_PORT, serverSelectionTimeoutMS=3000)

        client.admin.command("ping")
        print(f"[MongoDB] Conexión exitosa en {MONGO_HOST}:{MONGO_PORT}, DB sugerida: {MONGO_DB}")
        return client
    except PyMongoError as exc:
        print(f"[MongoDB] Error de conexión: {exc}")
        return None


def connect_cassandra():
    """Conecta a Cassandra y abre sesión al keyspace configurado.

    Returns:
        session o None si falla.
    """
    try:
        auth_provider = None
        if CASSANDRA_USER and CASSANDRA_PASSWORD:
            auth_provider = PlainTextAuthProvider(
                username=CASSANDRA_USER,
                password=CASSANDRA_PASSWORD,
            )

        cluster = Cluster(
            contact_points=[CASSANDRA_HOST],
            port=CASSANDRA_PORT,
            auth_provider=auth_provider,
        )

        session = cluster.connect()
        session.set_keyspace(CASSANDRA_KEYSPACE)
        print(
            f"[Cassandra] Conexión exitosa en {CASSANDRA_HOST}:{CASSANDRA_PORT}, "
            f"keyspace: {CASSANDRA_KEYSPACE}"
        )
        return session
    except Exception as exc:  # cassandra-driver lanza excepciones heterogéneas
        print(f"[Cassandra] Error de conexión: {exc}")
        return None


def connect_all() -> Tuple[Optional[MongoClient], Optional[object]]:
    """Conecta a MongoDB y Cassandra.

    Returns:
        Tupla: (mongo_client, cassandra_session)
    """
    mongo_client = connect_mongo()
    cassandra_session = connect_cassandra()
    return mongo_client, cassandra_session


if __name__ == "__main__":
    mongo_client, cassandra_session = connect_all()

    if mongo_client is not None:
        mongo_client.close()

    if cassandra_session is not None:
        cassandra_session.shutdown()
