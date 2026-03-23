"""
AWS End-of-Support (EOS) lifecycle data for various engines.
Maps engine versions to their EOS dates, recommended target versions,
upgrade types, and recommended instance types.

NOTE: These dates are approximate and should be verified against
the latest AWS documentation. Update this file regularly.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class VersionLifecycle:
    engine: str
    version: str
    eos_date: Optional[date]
    target_version: Optional[str]
    upgrade_type: Optional[str]  # "Major" or "Minor"
    recommend_instance_type: Optional[str]
    recommend_reason: str


# ---------------------------------------------------------------------------
# RDS MySQL
# ---------------------------------------------------------------------------
RDS_MYSQL = {
    "5.7": VersionLifecycle(
        engine="MySQL",
        version="5.7",
        eos_date=date(2024, 2, 29),
        target_version="8.0.36",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="MySQL 5.7 has reached end of standard support. Upgrade to 8.0 for security patches and performance improvements.",
    ),
    "8.0": VersionLifecycle(
        engine="MySQL",
        version="8.0",
        eos_date=date(2026, 7, 31),
        target_version="8.0.40",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Stay on latest 8.0 minor version for security and bug fixes.",
    ),
    "8.4": VersionLifecycle(
        engine="MySQL",
        version="8.4",
        eos_date=date(2032, 4, 30),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current LTS release, no immediate action needed.",
    ),
}

# ---------------------------------------------------------------------------
# RDS PostgreSQL
# ---------------------------------------------------------------------------
RDS_POSTGRESQL = {
    "11": VersionLifecycle(
        engine="PostgreSQL",
        version="11",
        eos_date=date(2024, 4, 9),
        target_version="16.4",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="PostgreSQL 11 has reached EOL. Upgrade to 16 for security, performance, and logical replication improvements.",
    ),
    "12": VersionLifecycle(
        engine="PostgreSQL",
        version="12",
        eos_date=date(2025, 2, 28),
        target_version="16.4",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="PostgreSQL 12 is approaching EOL. Upgrade to 16 for continued support.",
    ),
    "13": VersionLifecycle(
        engine="PostgreSQL",
        version="13",
        eos_date=date(2026, 2, 28),
        target_version="16.4",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="PostgreSQL 13 nearing EOL. Plan upgrade to 16.",
    ),
    "14": VersionLifecycle(
        engine="PostgreSQL",
        version="14",
        eos_date=date(2027, 2, 28),
        target_version="16.4",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Consider upgrading to 16 for improved query parallelism and logical replication.",
    ),
    "15": VersionLifecycle(
        engine="PostgreSQL",
        version="15",
        eos_date=date(2028, 2, 29),
        target_version="15.8",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Apply latest minor version for security patches.",
    ),
    "16": VersionLifecycle(
        engine="PostgreSQL",
        version="16",
        eos_date=date(2029, 2, 28),
        target_version="16.4",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Current stable release. Keep on latest minor.",
    ),
}

# ---------------------------------------------------------------------------
# RDS MariaDB
# ---------------------------------------------------------------------------
RDS_MARIADB = {
    "10.4": VersionLifecycle(
        engine="MariaDB",
        version="10.4",
        eos_date=date(2024, 6, 18),
        target_version="10.11.8",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="MariaDB 10.4 has reached EOL. Upgrade to 10.11 LTS.",
    ),
    "10.5": VersionLifecycle(
        engine="MariaDB",
        version="10.5",
        eos_date=date(2025, 6, 24),
        target_version="10.11.8",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="MariaDB 10.5 approaching EOL. Upgrade to 10.11 LTS.",
    ),
    "10.6": VersionLifecycle(
        engine="MariaDB",
        version="10.6",
        eos_date=date(2026, 7, 6),
        target_version="10.11.8",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Plan migration to 10.11 LTS before EOL.",
    ),
    "10.11": VersionLifecycle(
        engine="MariaDB",
        version="10.11",
        eos_date=date(2028, 2, 16),
        target_version="10.11.8",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Current LTS. Keep on latest minor.",
    ),
}

# ---------------------------------------------------------------------------
# ElastiCache Redis
# ---------------------------------------------------------------------------
ELASTICACHE_REDIS = {
    "6.0": VersionLifecycle(
        engine="Redis",
        version="6.0",
        eos_date=date(2025, 3, 31),
        target_version="7.1",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Redis 6.0 nearing EOL on ElastiCache. Upgrade to 7.1 for ACL improvements and performance.",
    ),
    "6.2": VersionLifecycle(
        engine="Redis",
        version="6.2",
        eos_date=date(2025, 8, 31),
        target_version="7.1",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Redis 6.2 approaching EOL. Upgrade to 7.1.",
    ),
    "7.0": VersionLifecycle(
        engine="Redis",
        version="7.0",
        eos_date=date(2026, 6, 30),
        target_version="7.1",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Upgrade to 7.1 for Sharded Pub/Sub and performance improvements.",
    ),
    "7.1": VersionLifecycle(
        engine="Redis",
        version="7.1",
        eos_date=date(2027, 12, 31),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current supported version.",
    ),
}

# ---------------------------------------------------------------------------
# ElastiCache Memcached
# ---------------------------------------------------------------------------
ELASTICACHE_MEMCACHED = {
    "1.6": VersionLifecycle(
        engine="Memcached",
        version="1.6",
        eos_date=None,
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current supported version.",
    ),
}

# ---------------------------------------------------------------------------
# EKS
# ---------------------------------------------------------------------------
EKS_KUBERNETES = {
    "1.24": VersionLifecycle(
        engine="Kubernetes",
        version="1.24",
        eos_date=date(2025, 1, 31),
        target_version="1.30",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="EKS 1.24 has reached end of standard support. Upgrade incrementally to 1.30.",
    ),
    "1.25": VersionLifecycle(
        engine="Kubernetes",
        version="1.25",
        eos_date=date(2025, 5, 1),
        target_version="1.30",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="EKS 1.25 approaching EOL. Plan sequential upgrade to 1.30.",
    ),
    "1.26": VersionLifecycle(
        engine="Kubernetes",
        version="1.26",
        eos_date=date(2025, 6, 11),
        target_version="1.30",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="EKS 1.26 approaching EOL. Plan upgrade to 1.30.",
    ),
    "1.27": VersionLifecycle(
        engine="Kubernetes",
        version="1.27",
        eos_date=date(2025, 7, 24),
        target_version="1.30",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="EKS 1.27 nearing EOL. Upgrade to 1.30.",
    ),
    "1.28": VersionLifecycle(
        engine="Kubernetes",
        version="1.28",
        eos_date=date(2025, 11, 26),
        target_version="1.31",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Plan upgrade path to 1.31.",
    ),
    "1.29": VersionLifecycle(
        engine="Kubernetes",
        version="1.29",
        eos_date=date(2026, 3, 23),
        target_version="1.31",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Plan upgrade to 1.31 before EOL.",
    ),
    "1.30": VersionLifecycle(
        engine="Kubernetes",
        version="1.30",
        eos_date=date(2026, 7, 23),
        target_version="1.31",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Consider upgrading to 1.31 for latest features.",
    ),
    "1.31": VersionLifecycle(
        engine="Kubernetes",
        version="1.31",
        eos_date=date(2026, 11, 23),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current supported version.",
    ),
}


# ---------------------------------------------------------------------------
# DocumentDB (MongoDB-compatible)
# ---------------------------------------------------------------------------
DOCUMENTDB = {
    "3.6": VersionLifecycle(
        engine="DocumentDB",
        version="3.6",
        eos_date=date(2024, 3, 31),
        target_version="5.0",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="DocumentDB 3.6 has reached EOL. Upgrade to 5.0 for transactions, flexible indexing, and continued support.",
    ),
    "4.0": VersionLifecycle(
        engine="DocumentDB",
        version="4.0",
        eos_date=date(2025, 4, 30),
        target_version="5.0",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="DocumentDB 4.0 approaching EOL. Upgrade to 5.0.",
    ),
    "5.0": VersionLifecycle(
        engine="DocumentDB",
        version="5.0",
        eos_date=None,
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current supported version.",
    ),
}

# ---------------------------------------------------------------------------
# OpenSearch Service
# ---------------------------------------------------------------------------
OPENSEARCH = {
    "Elasticsearch_5.6": VersionLifecycle(
        engine="Elasticsearch",
        version="5.6",
        eos_date=date(2023, 1, 31),
        target_version="OpenSearch_2.13",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Elasticsearch 5.6 has reached EOL. Migrate to OpenSearch 2.x.",
    ),
    "Elasticsearch_6.8": VersionLifecycle(
        engine="Elasticsearch",
        version="6.8",
        eos_date=date(2023, 8, 31),
        target_version="OpenSearch_2.13",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Elasticsearch 6.x has reached EOL. Migrate to OpenSearch 2.x.",
    ),
    "Elasticsearch_7.10": VersionLifecycle(
        engine="Elasticsearch",
        version="7.10",
        eos_date=date(2024, 4, 30),
        target_version="OpenSearch_2.13",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Elasticsearch 7.10 has reached EOL. Migrate to OpenSearch 2.x.",
    ),
    "OpenSearch_1.0": VersionLifecycle(
        engine="OpenSearch",
        version="1.0",
        eos_date=date(2024, 6, 30),
        target_version="OpenSearch_2.13",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="OpenSearch 1.x approaching EOL. Upgrade to 2.x.",
    ),
    "OpenSearch_1.3": VersionLifecycle(
        engine="OpenSearch",
        version="1.3",
        eos_date=date(2025, 3, 31),
        target_version="OpenSearch_2.13",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="OpenSearch 1.3 approaching EOL. Upgrade to 2.x.",
    ),
    "OpenSearch_2.3": VersionLifecycle(
        engine="OpenSearch",
        version="2.3",
        eos_date=date(2026, 3, 31),
        target_version="OpenSearch_2.13",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Upgrade to latest 2.x for bug fixes and features.",
    ),
    "OpenSearch_2.11": VersionLifecycle(
        engine="OpenSearch",
        version="2.11",
        eos_date=date(2026, 12, 31),
        target_version="OpenSearch_2.13",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Upgrade to latest 2.x minor version.",
    ),
    "OpenSearch_2.13": VersionLifecycle(
        engine="OpenSearch",
        version="2.13",
        eos_date=None,
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current supported version.",
    ),
}

# ---------------------------------------------------------------------------
# MSK (Managed Streaming for Apache Kafka)
# ---------------------------------------------------------------------------
MSK_KAFKA = {
    "2.6": VersionLifecycle(
        engine="Kafka",
        version="2.6",
        eos_date=date(2024, 3, 31),
        target_version="3.6.0",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Kafka 2.6 has reached EOL on MSK. Upgrade to 3.6.",
    ),
    "2.7": VersionLifecycle(
        engine="Kafka",
        version="2.7",
        eos_date=date(2024, 6, 30),
        target_version="3.6.0",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Kafka 2.7 has reached EOL on MSK. Upgrade to 3.6.",
    ),
    "2.8": VersionLifecycle(
        engine="Kafka",
        version="2.8",
        eos_date=date(2024, 11, 30),
        target_version="3.6.0",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Kafka 2.8 has reached EOL on MSK. Upgrade to 3.6.",
    ),
    "3.3": VersionLifecycle(
        engine="Kafka",
        version="3.3",
        eos_date=date(2025, 9, 30),
        target_version="3.6.0",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Kafka 3.3 approaching EOL. Upgrade to 3.6.",
    ),
    "3.5": VersionLifecycle(
        engine="Kafka",
        version="3.5",
        eos_date=date(2026, 6, 30),
        target_version="3.6.0",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Upgrade to 3.6 for latest features and fixes.",
    ),
    "3.6": VersionLifecycle(
        engine="Kafka",
        version="3.6",
        eos_date=None,
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current supported version.",
    ),
}

# ---------------------------------------------------------------------------
# Lambda Runtimes
# ---------------------------------------------------------------------------
LAMBDA_RUNTIMES = {
    "python3.7": VersionLifecycle(
        engine="Lambda",
        version="python3.7",
        eos_date=date(2023, 12, 4),
        target_version="python3.12",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Python 3.7 runtime deprecated. Migrate to Python 3.12.",
    ),
    "python3.8": VersionLifecycle(
        engine="Lambda",
        version="python3.8",
        eos_date=date(2024, 10, 14),
        target_version="python3.12",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Python 3.8 runtime deprecated. Migrate to Python 3.12.",
    ),
    "python3.9": VersionLifecycle(
        engine="Lambda",
        version="python3.9",
        eos_date=date(2025, 9, 30),
        target_version="python3.12",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Python 3.9 approaching deprecation. Migrate to Python 3.12.",
    ),
    "python3.10": VersionLifecycle(
        engine="Lambda",
        version="python3.10",
        eos_date=date(2026, 10, 4),
        target_version="python3.12",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Plan migration to Python 3.12.",
    ),
    "python3.11": VersionLifecycle(
        engine="Lambda",
        version="python3.11",
        eos_date=date(2027, 10, 24),
        target_version="python3.12",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Current supported. Consider Python 3.12 for latest features.",
    ),
    "python3.12": VersionLifecycle(
        engine="Lambda",
        version="python3.12",
        eos_date=date(2028, 10, 28),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current latest runtime.",
    ),
    "nodejs14.x": VersionLifecycle(
        engine="Lambda",
        version="nodejs14.x",
        eos_date=date(2023, 12, 4),
        target_version="nodejs20.x",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Node.js 14 runtime deprecated. Migrate to Node.js 20.",
    ),
    "nodejs16.x": VersionLifecycle(
        engine="Lambda",
        version="nodejs16.x",
        eos_date=date(2024, 6, 12),
        target_version="nodejs20.x",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Node.js 16 runtime deprecated. Migrate to Node.js 20.",
    ),
    "nodejs18.x": VersionLifecycle(
        engine="Lambda",
        version="nodejs18.x",
        eos_date=date(2025, 9, 30),
        target_version="nodejs20.x",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Node.js 18 approaching deprecation. Migrate to Node.js 20.",
    ),
    "nodejs20.x": VersionLifecycle(
        engine="Lambda",
        version="nodejs20.x",
        eos_date=date(2026, 10, 30),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current latest runtime.",
    ),
    "java8": VersionLifecycle(
        engine="Lambda",
        version="java8",
        eos_date=date(2024, 1, 8),
        target_version="java21",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Java 8 (non-AL2) runtime deprecated. Migrate to Java 21.",
    ),
    "java8.al2": VersionLifecycle(
        engine="Lambda",
        version="java8.al2",
        eos_date=date(2025, 2, 28),
        target_version="java21",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Java 8 AL2 runtime approaching deprecation. Migrate to Java 21.",
    ),
    "java11": VersionLifecycle(
        engine="Lambda",
        version="java11",
        eos_date=date(2025, 9, 30),
        target_version="java21",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="Java 11 approaching deprecation. Migrate to Java 21.",
    ),
    "java17": VersionLifecycle(
        engine="Lambda",
        version="java17",
        eos_date=date(2026, 10, 31),
        target_version="java21",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Plan migration to Java 21.",
    ),
    "java21": VersionLifecycle(
        engine="Lambda",
        version="java21",
        eos_date=date(2028, 9, 30),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current latest runtime.",
    ),
    "dotnet6": VersionLifecycle(
        engine="Lambda",
        version="dotnet6",
        eos_date=date(2024, 4, 12),
        target_version="dotnet8",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason=".NET 6 runtime deprecated. Migrate to .NET 8.",
    ),
    "dotnet8": VersionLifecycle(
        engine="Lambda",
        version="dotnet8",
        eos_date=date(2026, 11, 10),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current latest runtime.",
    ),
    "ruby3.2": VersionLifecycle(
        engine="Lambda",
        version="ruby3.2",
        eos_date=date(2026, 3, 31),
        target_version="ruby3.3",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Plan migration to Ruby 3.3.",
    ),
    "ruby3.3": VersionLifecycle(
        engine="Lambda",
        version="ruby3.3",
        eos_date=date(2027, 3, 31),
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current latest runtime.",
    ),
}

# ---------------------------------------------------------------------------
# Amazon MQ
# ---------------------------------------------------------------------------
AMAZONMQ_ACTIVEMQ = {
    "5.15": VersionLifecycle(
        engine="ActiveMQ",
        version="5.15",
        eos_date=date(2024, 3, 31),
        target_version="5.17.6",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="ActiveMQ 5.15 has reached EOL on Amazon MQ. Upgrade to 5.17.",
    ),
    "5.16": VersionLifecycle(
        engine="ActiveMQ",
        version="5.16",
        eos_date=date(2025, 6, 30),
        target_version="5.17.6",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="ActiveMQ 5.16 approaching EOL. Upgrade to 5.17.",
    ),
    "5.17": VersionLifecycle(
        engine="ActiveMQ",
        version="5.17",
        eos_date=None,
        target_version="5.17.6",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Current supported version. Keep on latest minor.",
    ),
}

AMAZONMQ_RABBITMQ = {
    "3.10": VersionLifecycle(
        engine="RabbitMQ",
        version="3.10",
        eos_date=date(2024, 7, 31),
        target_version="3.13",
        upgrade_type="Major",
        recommend_instance_type=None,
        recommend_reason="RabbitMQ 3.10 has reached EOL. Upgrade to 3.13.",
    ),
    "3.11": VersionLifecycle(
        engine="RabbitMQ",
        version="3.11",
        eos_date=date(2025, 3, 31),
        target_version="3.13",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="RabbitMQ 3.11 approaching EOL. Upgrade to 3.13.",
    ),
    "3.12": VersionLifecycle(
        engine="RabbitMQ",
        version="3.12",
        eos_date=date(2025, 12, 31),
        target_version="3.13",
        upgrade_type="Minor",
        recommend_instance_type=None,
        recommend_reason="Upgrade to 3.13 for quorum queues improvements.",
    ),
    "3.13": VersionLifecycle(
        engine="RabbitMQ",
        version="3.13",
        eos_date=None,
        target_version=None,
        upgrade_type=None,
        recommend_instance_type=None,
        recommend_reason="Current supported version.",
    ),
}


def _extract_major(version_str: str, engine: str) -> str:
    """Extract the major version key from a full version string."""
    parts = version_str.split(".")
    if engine in ("mysql", "mariadb"):
        # MySQL: 5.7.x -> "5.7", 8.0.x -> "8.0", 8.4.x -> "8.4"
        # MariaDB: 10.4.x -> "10.4", 10.11.x -> "10.11"
        return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]
    elif engine == "postgres":
        # PostgreSQL: 16.4 -> "16"
        return parts[0]
    elif engine in ("redis", "memcached"):
        return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]
    elif engine == "kubernetes":
        return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]
    elif engine == "docdb":
        # DocumentDB: 4.0.0 -> "4.0"
        return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]
    elif engine == "opensearch":
        # OpenSearch_2.11 or Elasticsearch_7.10 -> keep as-is from caller
        return version_str
    elif engine == "kafka":
        return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]
    elif engine == "lambda":
        # Lambda runtimes: python3.12, nodejs20.x, java21 -> keep as-is
        return version_str
    elif engine in ("activemq", "rabbitmq"):
        return ".".join(parts[:2]) if len(parts) >= 2 else parts[0]
    return parts[0]


# Map AWS engine names to our lifecycle dicts
_ENGINE_MAP = {
    "mysql": RDS_MYSQL,
    "postgres": RDS_POSTGRESQL,
    "mariadb": RDS_MARIADB,
    "redis": ELASTICACHE_REDIS,
    "memcached": ELASTICACHE_MEMCACHED,
    "kubernetes": EKS_KUBERNETES,
    "docdb": DOCUMENTDB,
    "opensearch": OPENSEARCH,
    "kafka": MSK_KAFKA,
    "lambda": LAMBDA_RUNTIMES,
    "activemq": AMAZONMQ_ACTIVEMQ,
    "rabbitmq": AMAZONMQ_RABBITMQ,
}

# Friendly engine names
ENGINE_DISPLAY_NAMES = {
    "mysql": "MySQL",
    "postgres": "PostgreSQL",
    "mariadb": "MariaDB",
    "redis": "Redis",
    "memcached": "Memcached",
    "kubernetes": "Kubernetes",
    "docdb": "DocumentDB",
    "opensearch": "OpenSearch",
    "kafka": "Kafka",
    "lambda": "Lambda",
    "activemq": "ActiveMQ",
    "rabbitmq": "RabbitMQ",
}


def lookup_lifecycle(engine: str, version: str) -> Optional[VersionLifecycle]:
    """
    Look up EOS lifecycle info for a given engine and version.
    engine: lowercase AWS engine name (mysql, postgres, redis, etc.)
    version: full version string (e.g. "8.0.35", "16.4", "7.1.0")
    """
    lifecycle_map = _ENGINE_MAP.get(engine.lower())
    if not lifecycle_map:
        return None
    major = _extract_major(version, engine.lower())
    return lifecycle_map.get(major)
