"""
AWS resource scanners for EOS (End-of-Support) checking.
Supports: RDS, ElastiCache, EKS, DocumentDB, OpenSearch, MSK, Lambda, Amazon MQ.
"""

import re
import boto3
from typing import Optional
from .eos_data import lookup_lifecycle, ENGINE_DISPLAY_NAMES
from .latest_versions import LatestVersionCache, _version_tuple


def _is_upgrade(current_version: str, target_version: str) -> bool:
    """Return True only if target_version is actually newer than current_version."""
    if not target_version:
        return False
    try:
        return _version_tuple(target_version) > _version_tuple(current_version)
    except (ValueError, TypeError):
        return True


def _determine_upgrade_type(current: str, target: str) -> str:
    """Determine if upgrade is Major or Minor based on version comparison."""
    try:
        cur = _version_tuple(current)
        tgt = _version_tuple(target)
        if cur[0] != tgt[0]:
            return "Major"
        return "Minor"
    except (ValueError, TypeError, IndexError):
        return "Major"


def _build_row(account, region, name, engine, resource_type, instance_type,
               engine_version, lifecycle, latest_version=None) -> dict:
    """Build a result row dict with dynamic latest version check."""
    target = latest_version or (lifecycle.target_version if lifecycle else None)
    reason = lifecycle.recommend_reason if lifecycle else "No EOS data available"

    # Check if already on latest version
    if target and not _is_upgrade(engine_version, target):
        target = None
        upgrade_type = None
        reason = "Already latest version"
    elif target:
        upgrade_type = _determine_upgrade_type(engine_version, target)
    else:
        upgrade_type = None

    return {
        "account": account,
        "region": region,
        "name": name,
        "engine": engine,
        "resource_type": resource_type,
        "instance_type": instance_type,
        "engine_version": engine_version,
        "eos_date": lifecycle.eos_date if lifecycle else None,
        "target_version": target,
        "upgrade_type": upgrade_type,
        "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
        "recommend_reason": reason,
    }


def _get_base_session(
    profile: str | None = None,
    access_key: str | None = None,
    secret_key: str | None = None,
) -> boto3.Session:
    """
    Create a base boto3 session from user-provided credentials.
    Priority: AK/SK > profile > default.
    """
    if access_key and secret_key:
        return boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
    if profile:
        return boto3.Session(profile_name=profile)
    return boto3.Session()


def _get_session(
    account: str,
    region: str,
    role_name: str = "OrganizationAccountAccessRole",
    base_session: boto3.Session | None = None,
):
    """
    Get a boto3 session for the target account/region.
    If account matches the current caller identity, return a direct session.
    Otherwise, assume a cross-account role.
    """
    if base_session is None:
        base_session = boto3.Session()

    sts = base_session.client("sts")
    current_account = sts.get_caller_identity()["Account"]

    if account == current_account:
        return boto3.Session(
            aws_access_key_id=base_session.get_credentials().access_key,
            aws_secret_access_key=base_session.get_credentials().secret_key,
            aws_session_token=base_session.get_credentials().token,
            region_name=region,
        ) if base_session.get_credentials() else boto3.Session(region_name=region)

    role_arn = f"arn:aws:iam::{account}:role/{role_name}"
    resp = sts.assume_role(RoleArn=role_arn, RoleSessionName="eos-scan")
    creds = resp["Credentials"]
    return boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
        region_name=region,
    )


def scan_rds(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan RDS instances and clusters for EOS info."""
    rds = session.client("rds")
    results = []

    # --- DB Instances ---
    paginator = rds.get_paginator("describe_db_instances")
    for page in paginator.paginate():
        for db in page["DBInstances"]:
            engine = db["Engine"]
            version = db["EngineVersion"]
            lifecycle = lookup_lifecycle(engine, version)
            latest = version_cache.get_latest_rds_version(engine) if version_cache else None
            results.append(_build_row(account, region, db["DBInstanceIdentifier"],
                ENGINE_DISPLAY_NAMES.get(engine, engine), "RDS", db["DBInstanceClass"],
                version, lifecycle, latest))

    # --- Aurora Clusters ---
    paginator = rds.get_paginator("describe_db_clusters")
    for page in paginator.paginate():
        for cluster in page["DBClusters"]:
            engine = cluster["Engine"]
            lookup_engine = engine.replace("aurora-", "").replace("postgresql", "postgres")
            version = cluster["EngineVersion"]
            lifecycle = lookup_lifecycle(lookup_engine, version)
            latest = version_cache.get_latest_aurora_version(engine) if version_cache else None

            instance_type = cluster.get("DBClusterInstanceClass", "Serverless" if "serverless" in engine else "N/A")
            results.append(_build_row(account, region, cluster["DBClusterIdentifier"],
                ENGINE_DISPLAY_NAMES.get(lookup_engine, engine), "Aurora", instance_type,
                version, lifecycle, latest))

    return results


def scan_elasticache(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan ElastiCache clusters/replication groups for EOS info."""
    ec = session.client("elasticache")
    results = []

    # --- Replication Groups (Redis) ---
    paginator = ec.get_paginator("describe_replication_groups")
    for page in paginator.paginate():
        for rg in page["ReplicationGroups"]:
            cache_node_type = "N/A"
            engine_version = "N/A"
            if rg.get("NodeGroups"):
                for ng in rg["NodeGroups"]:
                    if ng.get("NodeGroupMembers"):
                        member = ng["NodeGroupMembers"][0]
                        try:
                            cc_resp = ec.describe_cache_clusters(
                                CacheClusterId=member["CacheClusterId"],
                                ShowCacheNodeInfo=False,
                            )
                            cc = cc_resp["CacheClusters"][0]
                            cache_node_type = cc.get("CacheNodeType", "N/A")
                            engine_version = cc.get("EngineVersion", "N/A")
                        except Exception:
                            pass
                        break

            lifecycle = lookup_lifecycle("redis", engine_version)
            latest = version_cache.get_latest_elasticache_version("redis") if version_cache else None
            results.append(_build_row(account, region, rg["ReplicationGroupId"],
                "Redis", "ElastiCache", cache_node_type, engine_version, lifecycle, latest))

    # --- Standalone Memcached Clusters ---
    paginator = ec.get_paginator("describe_cache_clusters")
    for page in paginator.paginate(ShowCacheNodeInfo=False):
        for cc in page["CacheClusters"]:
            if cc["Engine"] != "memcached":
                continue
            version = cc.get("EngineVersion", "N/A")
            lifecycle = lookup_lifecycle("memcached", version)
            latest = version_cache.get_latest_elasticache_version("memcached") if version_cache else None
            results.append(_build_row(account, region, cc["CacheClusterId"],
                "Memcached", "ElastiCache", cc.get("CacheNodeType", "N/A"), version, lifecycle, latest))

    return results


def scan_eks(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan EKS clusters for EOS info."""
    eks = session.client("eks")
    results = []

    paginator = eks.get_paginator("list_clusters")
    for page in paginator.paginate():
        for cluster_name in page["clusters"]:
            cluster = eks.describe_cluster(name=cluster_name)["cluster"]
            version = cluster.get("version", "N/A")
            lifecycle = lookup_lifecycle("kubernetes", version)

            # Get node group instance types
            instance_types = set()
            try:
                ng_paginator = eks.get_paginator("list_nodegroups")
                for ng_page in ng_paginator.paginate(clusterName=cluster_name):
                    for ng_name in ng_page["nodegroups"]:
                        ng = eks.describe_nodegroup(
                            clusterName=cluster_name, nodegroupName=ng_name
                        )["nodegroup"]
                        for it in ng.get("instanceTypes", []):
                            instance_types.add(it)
            except Exception:
                pass

            it_str = ", ".join(sorted(instance_types)) if instance_types else "N/A"
            latest = version_cache.get_latest_eks_version() if version_cache else None
            results.append(_build_row(account, region, cluster_name,
                "Kubernetes", "EKS", it_str, version, lifecycle, latest))

    return results


def scan_documentdb(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan DocumentDB clusters for EOS info."""
    docdb = session.client("docdb")
    results = []
    latest = version_cache.get_latest_documentdb_version() if version_cache else None

    paginator = docdb.get_paginator("describe_db_clusters")
    for page in paginator.paginate():
        for cluster in page["DBClusters"]:
            version = cluster.get("EngineVersion", "N/A")
            lifecycle = lookup_lifecycle("docdb", version)

            instance_type = "N/A"
            if cluster.get("DBClusterMembers"):
                try:
                    member_id = cluster["DBClusterMembers"][0]["DBInstanceIdentifier"]
                    inst = docdb.describe_db_instances(DBInstanceIdentifier=member_id)
                    instance_type = inst["DBInstances"][0].get("DBInstanceClass", "N/A")
                except Exception:
                    pass

            results.append(_build_row(account, region, cluster["DBClusterIdentifier"],
                "DocumentDB", "DocumentDB", instance_type, version, lifecycle, latest))

    return results


def scan_opensearch(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan OpenSearch/Elasticsearch domains for EOS info."""
    client = session.client("opensearch")
    results = []

    domain_names = client.list_domain_names().get("DomainNames", [])
    if not domain_names:
        return results

    names = [d["DomainName"] for d in domain_names]
    domains = client.describe_domains(DomainNames=names).get("DomainStatusList", [])

    for domain in domains:
        engine_version = domain.get("EngineVersion", "N/A")
        # engine_version format: "OpenSearch_2.11" or "Elasticsearch_7.10"
        lifecycle = lookup_lifecycle("opensearch", engine_version)

        # Get instance type from cluster config
        cluster_config = domain.get("ClusterConfig", {})
        instance_type = cluster_config.get("InstanceType", "N/A")

        engine_name = "OpenSearch" if "OpenSearch" in engine_version else "Elasticsearch"
        latest = version_cache.get_latest_opensearch_version() if version_cache else None
        results.append(_build_row(account, region, domain["DomainName"],
            engine_name, "OpenSearch", instance_type, engine_version, lifecycle, latest))

    return results


def scan_msk(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan MSK Kafka clusters for EOS info."""
    client = session.client("kafka")
    results = []
    latest = version_cache.get_latest_msk_version() if version_cache else None

    paginator = client.get_paginator("list_clusters_v2")
    for page in paginator.paginate():
        for cluster in page.get("ClusterInfoList", []):
            cluster_name = cluster.get("ClusterName", "N/A")
            cluster_type = cluster.get("ClusterType", "PROVISIONED")

            if cluster_type == "PROVISIONED":
                prov = cluster.get("Provisioned", {})
                version = prov.get("CurrentBrokerSoftwareInfo", {}).get("KafkaVersion", "N/A")
                broker_nodes = prov.get("BrokerNodeGroupInfo", {})
                instance_type = broker_nodes.get("InstanceType", "N/A")
            else:
                version = "Serverless"
                instance_type = "Serverless"

            lifecycle = lookup_lifecycle("kafka", version)
            results.append(_build_row(account, region, cluster_name,
                "Kafka", "MSK", instance_type, version, lifecycle, latest))

    return results


def scan_lambda(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan Lambda functions for deprecated runtimes."""
    client = session.client("lambda")
    results = []

    paginator = client.get_paginator("list_functions")
    for page in paginator.paginate():
        for func in page["Functions"]:
            runtime = func.get("Runtime")
            if not runtime:
                continue

            lifecycle = lookup_lifecycle("lambda", runtime)
            if not lifecycle:
                continue

            # For Lambda, latest_version comes from eos_data (static per runtime family)
            # No dynamic API for "latest runtime", so use lifecycle target
            it_str = f'{func.get("MemorySize", "N/A")}MB / {func.get("Architectures", ["N/A"])[0]}'
            results.append(_build_row(account, region, func["FunctionName"],
                "Lambda", "Lambda", it_str, runtime, lifecycle))

    return results


def scan_amazonmq(session, account: str, region: str, version_cache: LatestVersionCache = None) -> list[dict]:
    """Scan Amazon MQ brokers (ActiveMQ, RabbitMQ) for EOS info."""
    client = session.client("mq")
    results = []

    paginator = client.get_paginator("list_brokers")
    for page in paginator.paginate():
        for broker_summary in page.get("BrokerSummaries", []):
            broker_id = broker_summary["BrokerId"]
            broker = client.describe_broker(BrokerId=broker_id)

            engine = broker.get("EngineType", "").upper()
            version = broker.get("EngineVersion", "N/A")
            lookup_engine = "activemq" if engine == "ACTIVEMQ" else "rabbitmq"
            lifecycle = lookup_lifecycle(lookup_engine, version)
            latest = version_cache.get_latest_amazonmq_version(engine) if version_cache else None

            results.append(_build_row(account, region, broker.get("BrokerName", broker_id),
                ENGINE_DISPLAY_NAMES.get(lookup_engine, engine), "Amazon MQ",
                broker.get("HostInstanceType", "N/A"), version, lifecycle, latest))

    return results


# Registry of scanner functions keyed by resource type
SCANNERS = {
    "rds": scan_rds,
    "elasticache": scan_elasticache,
    "eks": scan_eks,
    "documentdb": scan_documentdb,
    "opensearch": scan_opensearch,
    "msk": scan_msk,
    "lambda": scan_lambda,
    "amazonmq": scan_amazonmq,
}


def run_scan(
    accounts: list[str],
    regions: list[str],
    resource_types: list[str],
    role_name: str = "OrganizationAccountAccessRole",
    profile: str | None = None,
    access_key: str | None = None,
    secret_key: str | None = None,
) -> list[dict]:
    """
    Run EOS scan across accounts, regions, and resource types.
    Returns a list of row dicts ready for report generation.
    """
    base_session = _get_base_session(profile, access_key, secret_key)
    all_results = []
    for account in accounts:
        for region in regions:
            print(f"Scanning account={account} region={region} ...")
            try:
                session = _get_session(account, region, role_name, base_session)
            except Exception as e:
                print(f"  Failed to get session: {e}")
                continue

            version_cache = LatestVersionCache(session)
            print(f"  Fetching latest available versions ...")

            for rt in resource_types:
                scanner = SCANNERS.get(rt.lower())
                if not scanner:
                    print(f"  Unknown resource type: {rt}")
                    continue
                try:
                    rows = scanner(session, account, region, version_cache=version_cache)
                    print(f"  {rt}: found {len(rows)} resources")
                    all_results.extend(rows)
                except Exception as e:
                    print(f"  {rt}: error - {e}")

    return all_results
