[English](README.md) | [中文](README.zh-CN.md)

# EOS Skill - AWS End-of-Support Resource Scanner

Scan AWS resources for End-of-Support (EOS) status and generate an Excel upgrade report.

## Features

- Scan RDS instances & Aurora clusters (MySQL, PostgreSQL, MariaDB)
- Scan ElastiCache clusters (Redis, Memcached)
- Scan EKS Kubernetes clusters
- Scan DocumentDB clusters (MongoDB-compatible)
- Scan OpenSearch / Elasticsearch domains
- Scan MSK Kafka clusters
- Scan Lambda functions for deprecated runtimes
- Scan Amazon MQ brokers (ActiveMQ, RabbitMQ)
- Color-coded Excel report (Red=expired, Yellow=warning, Green=safe)
- Bilingual headers (English + Chinese)
- Cross-account scanning via IAM role assumption

## Prerequisites

```bash
pip install boto3 openpyxl
```

## Usage

### Method 1: Claude Code Skill

In Claude Code conversation, say:

```
eos report
```

Claude will ask for:
1. AWS credentials (profile or AK/SK)
2. Account ID(s)
3. Region(s)
4. Resource types

### Method 2: Command Line

#### Basic - single region

```bash
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 \
  --regions us-west-2
```

#### Multiple regions

```bash
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 \
  --regions us-west-2 us-west-1 ap-northeast-1
```

#### Multiple accounts + multiple regions

```bash
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 987654321098 \
  --regions us-west-2 us-east-1 ap-northeast-1
```

#### Specify output path

```bash
# Output to Desktop
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 \
  --regions us-west-2 \
  --output ~/Desktop/eos_report.xlsx

# Output to specific directory
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 \
  --regions us-west-2 us-west-1 \
  --output /tmp/reports/eos_report_prod.xlsx
```

#### Scan specific resource types only

```bash
# Only RDS and EKS
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 \
  --regions us-west-2 \
  --resource-types rds eks

# Only ElastiCache
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 \
  --regions us-west-2 \
  --resource-types elasticache
```

#### Using AK/SK instead of profile

```bash
python -m eos_skill.main \
  --access-key AKIAXXXXXXXX \
  --secret-key XXXXXXXXXXXXXXXX \
  --accounts 123456789012 \
  --regions us-west-2 us-west-1 \
  --output ~/Desktop/eos_report.xlsx
```

#### Cross-account with custom role name

```bash
python -m eos_skill.main \
  --profile my-profile \
  --accounts 123456789012 987654321098 \
  --regions us-west-2 \
  --role-name MyCustomCrossAccountRole
```

## All Options

| Option | Required | Description |
|--------|----------|-------------|
| `--accounts` | Yes | One or more AWS account IDs |
| `--regions` | Yes | One or more AWS regions |
| `--profile` | No | AWS CLI profile name |
| `--access-key` | No | AWS Access Key ID (requires `--secret-key`) |
| `--secret-key` | No | AWS Secret Access Key (requires `--access-key`) |
| `--resource-types` | No | `rds`, `elasticache`, `eks`, `documentdb`, `opensearch`, `msk`, `lambda`, `amazonmq` (default: all) |
| `--role-name` | No | Cross-account IAM role (default: `OrganizationAccountAccessRole`) |
| `--output` | No | Output file path (default: `eos_report_<timestamp>.xlsx`) |

## Report Columns

| # | Field | Description |
|---|-------|-------------|
| 1 | Account | AWS account ID |
| 2 | Region | AWS region |
| 3 | Cluster/Instance Name | Resource identifier |
| 4 | Engine | MySQL, PostgreSQL, Redis, etc. |
| 5 | Resource Type | RDS, Aurora, ElastiCache, EKS, DocumentDB, OpenSearch, MSK, Lambda, Amazon MQ |
| 6 | Instance Type | e.g., db.t3.medium |
| 7 | Engine Version | Current version |
| 8 | End of Support Date | EOS deadline |
| 9 | Target Engine Version | Recommended upgrade version |
| 10 | Upgrade Type | Major / Minor |
| 11 | Recommend Upgrade Instance Type | Suggested instance spec |
| 12 | Recommend Reason | Why upgrade is needed |

## Updating EOS Data

EOS lifecycle data is maintained in `eos_skill/eos_data.py`. Update this file when AWS announces new EOS dates.
