"""
AWS resource scanners for EOS (End-of-Support) checking.
Supports: RDS, ElastiCache, EKS.
"""

import boto3
from typing import Optional
from .eos_data import lookup_lifecycle, ENGINE_DISPLAY_NAMES


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


def scan_rds(session, account: str, region: str) -> list[dict]:
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

            row = {
                "account": account,
                "region": region,
                "name": db["DBInstanceIdentifier"],
                "engine": ENGINE_DISPLAY_NAMES.get(engine, engine),
                "resource_type": "RDS",
                "instance_type": db["DBInstanceClass"],
                "engine_version": version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

    # --- Aurora Clusters ---
    paginator = rds.get_paginator("describe_db_clusters")
    for page in paginator.paginate():
        for cluster in page["DBClusters"]:
            engine = cluster["Engine"]
            # aurora-mysql -> mysql, aurora-postgresql -> postgres
            lookup_engine = engine.replace("aurora-", "").replace("postgresql", "postgres")
            version = cluster["EngineVersion"]
            lifecycle = lookup_lifecycle(lookup_engine, version)

            row = {
                "account": account,
                "region": region,
                "name": cluster["DBClusterIdentifier"],
                "engine": ENGINE_DISPLAY_NAMES.get(lookup_engine, engine),
                "resource_type": "Aurora",
                "instance_type": cluster.get("DBClusterInstanceClass", "Serverless" if "serverless" in engine else "N/A"),
                "engine_version": version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

    return results


def scan_elasticache(session, account: str, region: str) -> list[dict]:
    """Scan ElastiCache clusters/replication groups for EOS info."""
    ec = session.client("elasticache")
    results = []

    # --- Replication Groups (Redis) ---
    paginator = ec.get_paginator("describe_replication_groups")
    for page in paginator.paginate():
        for rg in page["ReplicationGroups"]:
            # Get details from the first node group's member
            cache_node_type = "N/A"
            engine_version = "N/A"
            if rg.get("NodeGroups"):
                for ng in rg["NodeGroups"]:
                    if ng.get("NodeGroupMembers"):
                        member = ng["NodeGroupMembers"][0]
                        # Need to describe the cache cluster for version info
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

            row = {
                "account": account,
                "region": region,
                "name": rg["ReplicationGroupId"],
                "engine": "Redis",
                "resource_type": "ElastiCache",
                "instance_type": cache_node_type,
                "engine_version": engine_version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

    # --- Standalone Memcached Clusters ---
    paginator = ec.get_paginator("describe_cache_clusters")
    for page in paginator.paginate(ShowCacheNodeInfo=False):
        for cc in page["CacheClusters"]:
            if cc["Engine"] != "memcached":
                continue
            version = cc.get("EngineVersion", "N/A")
            lifecycle = lookup_lifecycle("memcached", version)

            row = {
                "account": account,
                "region": region,
                "name": cc["CacheClusterId"],
                "engine": "Memcached",
                "resource_type": "ElastiCache",
                "instance_type": cc.get("CacheNodeType", "N/A"),
                "engine_version": version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

    return results


def scan_eks(session, account: str, region: str) -> list[dict]:
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

            row = {
                "account": account,
                "region": region,
                "name": cluster_name,
                "engine": "Kubernetes",
                "resource_type": "EKS",
                "instance_type": ", ".join(sorted(instance_types)) if instance_types else "N/A",
                "engine_version": version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

    return results


def scan_documentdb(session, account: str, region: str) -> list[dict]:
    """Scan DocumentDB clusters for EOS info."""
    rds = session.client("rds")
    results = []

    paginator = rds.get_paginator("describe_db_clusters")
    for page in paginator.paginate(Filters=[{"Name": "engine", "Values": ["docdb"]}]):
        for cluster in page["DBClusters"]:
            version = cluster.get("EngineVersion", "N/A")
            lifecycle = lookup_lifecycle("docdb", version)

            # Get instance type from cluster members
            instance_type = "N/A"
            if cluster.get("DBClusterMembers"):
                try:
                    member_id = cluster["DBClusterMembers"][0]["DBInstanceIdentifier"]
                    inst = rds.describe_db_instances(DBInstanceIdentifier=member_id)
                    instance_type = inst["DBInstances"][0].get("DBInstanceClass", "N/A")
                except Exception:
                    pass

            row = {
                "account": account,
                "region": region,
                "name": cluster["DBClusterIdentifier"],
                "engine": "DocumentDB",
                "resource_type": "DocumentDB",
                "instance_type": instance_type,
                "engine_version": version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

    return results


def scan_opensearch(session, account: str, region: str) -> list[dict]:
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

        row = {
            "account": account,
            "region": region,
            "name": domain["DomainName"],
            "engine": "OpenSearch" if "OpenSearch" in engine_version else "Elasticsearch",
            "resource_type": "OpenSearch",
            "instance_type": instance_type,
            "engine_version": engine_version,
            "eos_date": lifecycle.eos_date if lifecycle else None,
            "target_version": lifecycle.target_version if lifecycle else None,
            "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
            "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
            "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
        }
        results.append(row)

    return results


def scan_msk(session, account: str, region: str) -> list[dict]:
    """Scan MSK Kafka clusters for EOS info."""
    client = session.client("kafka")
    results = []

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
                # Serverless
                version = "Serverless"
                instance_type = "Serverless"

            lifecycle = lookup_lifecycle("kafka", version)

            row = {
                "account": account,
                "region": region,
                "name": cluster_name,
                "engine": "Kafka",
                "resource_type": "MSK",
                "instance_type": instance_type,
                "engine_version": version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

    return results


def scan_lambda(session, account: str, region: str) -> list[dict]:
    """Scan Lambda functions for deprecated runtimes."""
    client = session.client("lambda")
    results = []

    paginator = client.get_paginator("list_functions")
    for page in paginator.paginate():
        for func in page["Functions"]:
            runtime = func.get("Runtime")
            if not runtime:
                continue  # Skip container image or custom runtimes

            lifecycle = lookup_lifecycle("lambda", runtime)
            if not lifecycle:
                continue  # Skip unknown/current runtimes with no EOS concern

            row = {
                "account": account,
                "region": region,
                "name": func["FunctionName"],
                "engine": "Lambda",
                "resource_type": "Lambda",
                "instance_type": f'{func.get("MemorySize", "N/A")}MB / {func.get("Architectures", ["N/A"])[0]}',
                "engine_version": runtime,
                "eos_date": lifecycle.eos_date,
                "target_version": lifecycle.target_version,
                "upgrade_type": lifecycle.upgrade_type,
                "recommend_instance_type": None,
                "recommend_reason": lifecycle.recommend_reason,
            }
            results.append(row)

    return results


def scan_amazonmq(session, account: str, region: str) -> list[dict]:
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

            row = {
                "account": account,
                "region": region,
                "name": broker.get("BrokerName", broker_id),
                "engine": ENGINE_DISPLAY_NAMES.get(lookup_engine, engine),
                "resource_type": "Amazon MQ",
                "instance_type": broker.get("HostInstanceType", "N/A"),
                "engine_version": version,
                "eos_date": lifecycle.eos_date if lifecycle else None,
                "target_version": lifecycle.target_version if lifecycle else None,
                "upgrade_type": lifecycle.upgrade_type if lifecycle else None,
                "recommend_instance_type": lifecycle.recommend_instance_type if lifecycle else None,
                "recommend_reason": lifecycle.recommend_reason if lifecycle else "No EOS data available",
            }
            results.append(row)

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

            for rt in resource_types:
                scanner = SCANNERS.get(rt.lower())
                if not scanner:
                    print(f"  Unknown resource type: {rt}")
                    continue
                try:
                    rows = scanner(session, account, region)
                    print(f"  {rt}: found {len(rows)} resources")
                    all_results.extend(rows)
                except Exception as e:
                    print(f"  {rt}: error - {e}")

    return all_results
