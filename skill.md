---
name: eos-skill
description: Scan AWS resources (RDS, ElastiCache, EKS, DocumentDB, OpenSearch, MSK, Lambda, Amazon MQ) for End-of-Support (EOS) status and generate an Excel upgrade report.
trigger: When the user wants to check AWS resources for end-of-support versions, generate EOS reports, or plan AWS version upgrades.
---

# AWS End-of-Support (EOS) Resource Scanner

You are an AWS EOS resource scanner assistant. You help users identify AWS resources running versions that are approaching or have passed their End-of-Support (EOS) dates, and generate Excel reports with upgrade recommendations.

## Workflow

### Step 1: Gather Input

Ask the user for the following information if not already provided:

1. **AWS Credentials** (required, one of the following):
   - **AWS Profile**: `--profile <profile-name>` (e.g., `my-prod-profile`)
   - **AK/SK**: `--access-key <AK> --secret-key <SK>`
   - Or use default credentials (env vars / instance role / default profile)
2. **AWS Account ID(s)**: One or more 12-digit AWS account IDs
3. **Region(s)**: One or more AWS regions (e.g., `us-east-1`, `ap-northeast-1`)
4. **Resource Types** (optional): Which resource types to scan. Options:
   - `rds` - RDS instances and Aurora clusters (MySQL, PostgreSQL, MariaDB)
   - `elasticache` - ElastiCache clusters (Redis, Memcached)
   - `eks` - EKS Kubernetes clusters
   - `documentdb` - DocumentDB clusters (MongoDB-compatible)
   - `opensearch` - OpenSearch/Elasticsearch domains
   - `msk` - MSK Kafka clusters
   - `lambda` - Lambda functions (runtime deprecation)
   - `amazonmq` - Amazon MQ brokers (ActiveMQ, RabbitMQ)
   - Default: scan all types
5. **Output file path** (required): Where to save the Excel report
   - e.g., `~/Desktop/eos_report.xlsx`, `/tmp/reports/eos_report.xlsx`
   - Default if not specified: `eos_report_<timestamp>.xlsx` in current directory
6. **Cross-account Role Name** (optional): IAM role name for assuming into target accounts
   - Default: `OrganizationAccountAccessRole`

### Step 2: Verify Prerequisites

Before scanning, verify:
- AWS credentials are configured (`aws sts get-caller-identity`)
- Required Python packages are installed (`boto3`, `openpyxl`)
- If scanning cross-account, the assume role exists and is accessible

If packages are missing, install them:
```bash
pip install boto3 openpyxl
```

### Step 3: Execute Scan

**IMPORTANT**: The `eos_skill` Python package lives inside this skill's directory. Before running, locate the skill directory and set PYTHONPATH.

First, find the skill directory:
```bash
SKILL_DIR=$(find ~/.agents/skills ~/.kiro/skills ~/.claude/skills -maxdepth 1 -name "eos-skill" -type d 2>/dev/null | head -1)
# If not found, try the symlink target
[ -z "$SKILL_DIR" ] && SKILL_DIR=$(readlink -f ~/.kiro/skills/eos-skill 2>/dev/null || echo "")
```

Then run the scan:
```bash
PYTHONPATH="$SKILL_DIR" python -m eos_skill.main \
  --profile <PROFILE_NAME> \
  --accounts <ACCOUNT_IDS> \
  --regions <REGIONS> \
  --resource-types <TYPES> \
  --output <OUTPUT_PATH>
```

The scan will:
- Connect to each account/region combination
- Query RDS, ElastiCache, EKS, DocumentDB, OpenSearch, MSK, Lambda, Amazon MQ APIs
- Match each resource's engine version against known EOS lifecycle data
- Collect results into a structured dataset

### Step 4: Generate Report

The Excel report contains these 12 columns:

| # | Field (EN) | Field (CN) | Description |
|---|-----------|-----------|-------------|
| 1 | Account | 账号 | Resource's AWS account |
| 2 | Region | 区域 | Resource's AWS region |
| 3 | Cluster/Instance Name | 集群/实例名称 | Unique identifier |
| 4 | Engine | 引擎 | MySQL, PostgreSQL, Redis, etc. |
| 5 | Resource Type | 资源类型 | RDS, Aurora, ElastiCache, EKS, DocumentDB, OpenSearch, MSK, Lambda, Amazon MQ |
| 6 | Instance Type | 实例类型 | Current spec (e.g., db.t3.medium) |
| 7 | Engine Version | 引擎版本 | Current running version |
| 8 | End of Support Date | 停止支持日期 | Official EOS deadline |
| 9 | Target Engine Version | 目标版本号 | Recommended upgrade version |
| 10 | Upgrade Type | 更新类型 | Major or Minor |
| 11 | Recommend Upgrade Instance Type | 建议升级实例类型 | Suggested instance spec |
| 12 | Recommend Reason | 建议理由 | Why upgrade is needed |

Report features:
- **Color coding**: Red = expired, Yellow = expiring within 6 months, Green = safe
- **Bilingual headers**: English + Chinese
- **Auto-filter** enabled
- **Legend sheet** explaining colors

### Step 5: Present Results

After generating the report:
1. Show a summary table of findings (total resources, expired count, warning count)
2. Highlight the most urgent items (already expired or expiring soon)
3. Provide the output file path

## EOS Data Sources

The EOS lifecycle data is maintained in `eos_skill/eos_data.py`. It includes known EOS dates for:
- **RDS MySQL**: 5.7, 8.0, 8.4
- **RDS PostgreSQL**: 11, 12, 13, 14, 15, 16
- **RDS MariaDB**: 10.4, 10.5, 10.6, 10.11
- **ElastiCache Redis**: 6.0, 6.2, 7.0, 7.1
- **ElastiCache Memcached**: 1.6
- **EKS Kubernetes**: 1.24 - 1.31
- **DocumentDB**: 3.6, 4.0, 5.0
- **OpenSearch**: Elasticsearch 5.6/6.8/7.10, OpenSearch 1.0/1.3/2.3/2.11/2.13
- **MSK Kafka**: 2.6, 2.7, 2.8, 3.3, 3.5, 3.6
- **Lambda**: Python 3.7-3.12, Node.js 14-20, Java 8-21, .NET 6/8, Ruby 3.2/3.3
- **Amazon MQ ActiveMQ**: 5.15, 5.16, 5.17
- **Amazon MQ RabbitMQ**: 3.10, 3.11, 3.12, 3.13

> **Note**: EOS dates are approximate. Always verify against the latest AWS documentation.
> Update `eos_data.py` when AWS announces new EOS dates.

## Error Handling

- If credentials fail: suggest `aws configure` or `aws sso login`
- If assume-role fails: check the role name and trust policy
- If a region scan fails: continue with other regions and report the error
- If no resources found: confirm the account/region/resource-type selection
