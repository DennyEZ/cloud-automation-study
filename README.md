# ☁️ FinOps Bot - Cloud Cost Optimizer

A Python-based cloud cost optimization tool that analyzes AWS instance inventory, identifies over-budget resources, and automatically shuts down idle servers to reduce costs.

---

## 🎯 Features

- **Budget Analysis** - Compares total cloud spend against monthly budget
- **Over-Budget Detection** - Flags expensive instances (>$100/month)
- **Idle Resource Detection** - Finds running instances with CPU usage < 5%
- **Automated Optimization** - Shuts down idle instances and calculates savings
- **Smart Recommendations** - Suggests cost optimization strategies

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core application logic |
| Docker | Containerization |
| JSON | Cloud inventory data store |

## 📁 Project Structure

```
cloud-automation-study/
├── cloud_cost_optimizer.py      # Main Python script
├── cloud_inventory.json         # Input: Fake AWS instance data (never modified)
├── cloud_inventory_output.json  # Output: Generated results (git-ignored)
├── Dockerfile                   # Container definition
├── .dockerignore                # Docker build exclusions
├── .gitignore                   # Git exclusions
└── README.md                    # This file
```

> **Note:** The script reads from `cloud_inventory.json` and writes changes to `cloud_inventory_output.json`. This keeps the original data clean for testing!

## 🚀 Quick Start

### Run Locally (Python)

```bash
# Interactive mode (prompts for confirmation)
python cloud_cost_optimizer.py

# Auto mode (shuts down idle instances automatically)
python cloud_cost_optimizer.py --auto

# Dry run (analysis only, no changes)
python cloud_cost_optimizer.py --dry-run
```

### Run with Docker 🐳

```bash
# Build the image
docker build -t finops-bot .

# Run the container (auto mode)
docker run finops-bot

# Run in dry-run mode
docker run finops-bot python cloud_cost_optimizer.py --dry-run

# Run interactive mode
docker run -it finops-bot python cloud_cost_optimizer.py
```

## 📊 Sample Output

```
======================================================================
☁️  CLOUD COST OPTIMIZATION REPORT
======================================================================
📅 Generated: 2026-02-01 13:41:39

📊 BUDGET ANALYSIS
----------------------------------------
   Monthly Budget:     $5,000.00
   Total Monthly Cost: $3,081.11
   Budget Remaining:   $1,918.89
   Instances:          9 running / 10 total
   ✅ Within budget

😴 IDLE INSTANCES (CPU < 5.0%, Status: Running)
----------------------------------------
   🔸 ml-training-gpu      $2,233.80/month  (4.2% CPU)
   🔸 legacy-api-server    $140.16/month    (3.2% CPU)
   🔸 analytics-worker-01  $124.10/month    (1.5% CPU)

🔧 OPTIMIZATION ACTIONS TAKEN
----------------------------------------
   ✅ Shut down 5 idle instance(s)
   💵 Monthly Savings: $2,649.88
   💵 Annual Savings:  $31,798.56
```

## 🎓 DevOps Skills Demonstrated

| Skill | How It's Shown |
|-------|----------------|
| **Cost Optimization** | Core focus - identifies waste and calculates savings |
| **Resource Monitoring** | Analyzes CPU metrics to find idle servers |
| **Automation** | Auto-shutdown mode, CLI arguments |
| **Containerization** | Dockerfile with security best practices |
| **Python** | Clean, documented, production-style code |
| **Cloud Knowledge** | Realistic AWS instance types (t3, c5, p3, r5) |

## 🔒 Docker Security Best Practices

The Dockerfile follows production security standards:
- ✅ Uses slim base image (`python:3.11-slim`)
- ✅ Runs as non-root user (`appuser`)
- ✅ Includes health check
- ✅ Sets proper environment variables
- ✅ Uses `.dockerignore` to minimize image size

## 📈 Future Improvements

- [ ] Integration with AWS SDK (boto3) for real API calls
- [ ] Slack/Discord alerts when budget exceeded
- [ ] Scheduled runs with cron/Lambda
- [ ] Terraform infrastructure provisioning
- [ ] Prometheus metrics export

---

**Author:** Deniz  
**Purpose:** Cloud Automation Study