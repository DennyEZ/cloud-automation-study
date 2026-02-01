#!/usr/bin/env python3
"""
Cloud Cost Optimizer - AWS Instance Budget & Resource Monitor

This script demonstrates DevOps cost optimization skills by:
1. Reading a cloud inventory from JSON
2. Identifying over-budget instances
3. Detecting underutilized servers (running but low CPU)
4. Simulating shutdown of idle resources
5. Calculating potential cost savings

Author: Deniz
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

# Configuration
INVENTORY_FILE = "cloud_inventory.json"  # Input file 
OUTPUT_FILE = "cloud_inventory_output.json"  # Output file (contains changes)
CPU_THRESHOLD = 5.0  # Servers with CPU usage below this are considered idle
COST_THRESHOLD_HIGH = 100.0  # Monthly cost above this is flagged as expensive


def load_inventory(file_path: str) -> dict:
    """Load cloud inventory from JSON file."""
    try:
        # Use utf-8-sig to handle Windows BOM (Byte Order Mark)
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Inventory file '{file_path}' not found!")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in inventory file: {e}")
        raise


def save_inventory(file_path: str, data: dict) -> None:
    """Save updated inventory back to JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"💾 Inventory saved to {file_path}")


def analyze_budget(inventory: dict) -> dict:
    """Analyze instances against budget and identify over-budget resources."""
    cloud_data = inventory["cloud_inventory"]
    budget = cloud_data["monthly_budget"]
    instances = cloud_data["instances"]
    
    # Calculate total costs
    total_monthly_cost = sum(inst["monthly_cost"] for inst in instances)
    running_instances = [inst for inst in instances if inst["status"] == "running"]
    running_cost = sum(inst["monthly_cost"] for inst in running_instances)
    
    # Identify expensive instances
    over_budget_instances = [
        inst for inst in instances 
        if inst["monthly_cost"] > COST_THRESHOLD_HIGH
    ]
    
    return {
        "budget": budget,
        "total_cost": total_monthly_cost,
        "running_cost": running_cost,
        "is_over_budget": total_monthly_cost > budget,
        "budget_remaining": budget - total_monthly_cost,
        "over_budget_instances": over_budget_instances,
        "running_count": len(running_instances),
        "total_count": len(instances)
    }


def find_idle_instances(inventory: dict) -> list:
    """Find running instances with CPU usage below threshold."""
    instances = inventory["cloud_inventory"]["instances"]
    
    idle_instances = [
        inst for inst in instances
        if inst["status"] == "running" and inst["cpu_usage"] < CPU_THRESHOLD
    ]
    
    return idle_instances


def shutdown_idle_instances(inventory: dict, idle_instances: list) -> float:
    """
    Simulate shutting down idle instances.
    Updates the inventory and returns total savings.
    """
    total_savings = 0.0
    
    for idle_inst in idle_instances:
        # Find and update the instance in inventory
        for inst in inventory["cloud_inventory"]["instances"]:
            if inst["instance_id"] == idle_inst["instance_id"]:
                inst["status"] = "stopped"
                inst["previous_monthly_cost"] = inst["monthly_cost"]
                total_savings += inst["monthly_cost"]
                inst["monthly_cost"] = 0.0
                inst["shutdown_reason"] = "auto-optimization"
                inst["shutdown_timestamp"] = datetime.now().isoformat()
                break
    
    return total_savings


def print_report_header():
    """Print the report header."""
    print("\n" + "=" * 70)
    print("☁️  CLOUD COST OPTIMIZATION REPORT")
    print("=" * 70)
    print(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 70)


def print_budget_analysis(analysis: dict):
    """Print budget analysis section."""
    print("\n📊 BUDGET ANALYSIS")
    print("-" * 40)
    print(f"   Monthly Budget:     ${analysis['budget']:,.2f}")
    print(f"   Total Monthly Cost: ${analysis['total_cost']:,.2f}")
    print(f"   Running Cost:       ${analysis['running_cost']:,.2f}")
    print(f"   Budget Remaining:   ${analysis['budget_remaining']:,.2f}")
    print(f"   Instances:          {analysis['running_count']} running / {analysis['total_count']} total")
    
    if analysis['is_over_budget']:
        overage = abs(analysis['budget_remaining'])
        print(f"\n   ⚠️  WARNING: Over budget by ${overage:,.2f}!")
    else:
        print(f"\n   ✅ Within budget")


def print_expensive_instances(instances: list):
    """Print instances that are over the cost threshold."""
    if not instances:
        print("\n✅ No instances exceed the cost threshold.")
        return
    
    print(f"\n💰 EXPENSIVE INSTANCES (>${COST_THRESHOLD_HIGH}/month)")
    print("-" * 40)
    
    for inst in sorted(instances, key=lambda x: x["monthly_cost"], reverse=True):
        status_icon = "🟢" if inst["status"] == "running" else "🔴"
        print(f"\n   {status_icon} {inst['name']}")
        print(f"      Instance ID: {inst['instance_id']}")
        print(f"      Type:        {inst['type']}")
        print(f"      Monthly:     ${inst['monthly_cost']:,.2f}")
        print(f"      CPU Usage:   {inst['cpu_usage']}%")
        print(f"      Owner:       {inst['owner']}")
        print(f"      Environment: {inst['environment']}")


def print_idle_instances(instances: list):
    """Print idle instances that could be shut down."""
    if not instances:
        print("\n✅ No idle instances detected.")
        return
    
    print(f"\n😴 IDLE INSTANCES (CPU < {CPU_THRESHOLD}%, Status: Running)")
    print("-" * 40)
    
    potential_savings = sum(inst["monthly_cost"] for inst in instances)
    
    for inst in instances:
        print(f"\n   🔸 {inst['name']}")
        print(f"      Instance ID: {inst['instance_id']}")
        print(f"      Type:        {inst['type']}")
        print(f"      CPU Usage:   {inst['cpu_usage']}%")
        print(f"      Monthly:     ${inst['monthly_cost']:,.2f}")
        print(f"      Environment: {inst['environment']}")
    
    print(f"\n   💡 Potential Monthly Savings: ${potential_savings:,.2f}")


def print_optimization_results(idle_count: int, savings: float):
    """Print optimization results after shutdown."""
    print("\n🔧 OPTIMIZATION ACTIONS TAKEN")
    print("-" * 40)
    print(f"   ✅ Shut down {idle_count} idle instance(s)")
    print(f"   💵 Monthly Savings: ${savings:,.2f}")
    print(f"   💵 Annual Savings:  ${savings * 12:,.2f}")


def print_recommendations(analysis: dict, idle_instances: list):
    """Print cost optimization recommendations."""
    print("\n📋 RECOMMENDATIONS")
    print("-" * 40)
    
    recommendations = []
    
    if analysis['is_over_budget']:
        recommendations.append("🔴 CRITICAL: Reduce spending to meet budget target")
    
    if idle_instances:
        recommendations.append(f"🟡 Review {len(idle_instances)} idle instances for shutdown")
    
    expensive = analysis['over_budget_instances']
    gpu_instances = [i for i in expensive if 'gpu' in i['name'].lower() or i['type'].startswith('p')]
    if gpu_instances:
        recommendations.append("🟡 Consider using spot instances for GPU workloads")
    
    dev_idle = [i for i in idle_instances if i['environment'] in ['development', 'staging', 'ci-cd']]
    if dev_idle:
        recommendations.append("🟢 Implement auto-stop for non-production environments")
    
    if not recommendations:
        recommendations.append("✅ Infrastructure is well-optimized!")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Cloud Cost Optimizer - Analyze and optimize AWS instance costs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cloud_cost_optimizer.py              # Interactive mode
  python cloud_cost_optimizer.py --auto       # Auto-shutdown idle instances
  python cloud_cost_optimizer.py --dry-run    # Report only, no changes
        """
    )
    parser.add_argument(
        "--auto", 
        action="store_true",
        help="Automatically shut down idle instances without prompting"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true", 
        help="Run analysis only, do not make any changes"
    )
    return parser.parse_args()


def main():
    """Main function to run the cloud cost optimizer."""
    args = parse_arguments()
    
    script_dir = Path(__file__).parent
    inventory_path = script_dir / INVENTORY_FILE
    output_path = script_dir / OUTPUT_FILE
    
    # Load inventory
    print("📂 Loading cloud inventory...")
    inventory = load_inventory(inventory_path)
    
    # Print report header
    print_report_header()
    
    # Analyze budget
    analysis = analyze_budget(inventory)
    print_budget_analysis(analysis)
    
    # Show expensive instances
    print_expensive_instances(analysis['over_budget_instances'])
    
    # Find idle instances
    idle_instances = find_idle_instances(inventory)
    print_idle_instances(idle_instances)
    
    # Simulate shutdown of idle instances
    if idle_instances:
        print("\n" + "=" * 70)
        
        if args.dry_run:
            print("   🔍 DRY RUN MODE - No changes will be made")
        elif args.auto:
            print("   🤖 AUTO MODE - Shutting down idle instances...")
            savings = shutdown_idle_instances(inventory, idle_instances)
            save_inventory(output_path, inventory)
            print_optimization_results(len(idle_instances), savings)
        else:
            # Interactive mode
            user_input = input("🔄 Shut down idle instances? (yes/no): ").strip().lower()
            
            if user_input in ['yes', 'y']:
                savings = shutdown_idle_instances(inventory, idle_instances)
                save_inventory(output_path, inventory)
                print_optimization_results(len(idle_instances), savings)
            else:
                print("   ℹ️  No changes made. Idle instances remain running.")
    
    # Print recommendations
    print_recommendations(analysis, idle_instances)
    
    # Footer
    print("\n" + "=" * 70)
    print("📊 Report Complete - DevOps Cost Optimization Demo")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
