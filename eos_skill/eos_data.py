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
    return parts[0]


# Map AWS engine names to our lifecycle dicts
_ENGINE_MAP = {
    "mysql": RDS_MYSQL,
    "postgres": RDS_POSTGRESQL,
    "mariadb": RDS_MARIADB,
    "redis": ELASTICACHE_REDIS,
    "memcached": ELASTICACHE_MEMCACHED,
    "kubernetes": EKS_KUBERNETES,
}

# Friendly engine names
ENGINE_DISPLAY_NAMES = {
    "mysql": "MySQL",
    "postgres": "PostgreSQL",
    "mariadb": "MariaDB",
    "redis": "Redis",
    "memcached": "Memcached",
    "kubernetes": "Kubernetes",
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
