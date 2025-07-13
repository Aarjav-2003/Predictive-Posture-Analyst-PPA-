import json
import networkx as nx
from ppa_graph import G  # Import the graph built from ppa_graph.py

# ----------- RISK SCORING FUNCTION -----------
def score_path(path):
    score = 10  # Base score
    if "user:root" in path:
        score += 15
    if any("cronjob" in node for node in path):
        score += 5
    if len(path) <= 3:
        score += 10
    return score

# ----------- MAIN ATTACK SIMULATOR -----------
def simulate_attack_paths(start_node):
    if not G.has_node(start_node):
        print(f"[!] Node '{start_node}' not found in graph.")
        return

    print(f"\n[🔍] Simulating attack paths from: {start_node}\n")
    targets = ["user:root", "cronjob", "firewall_rule", "port", "service"]
    attack_paths = []

    for target_node in G.nodes():
        if target_node == start_node:
            continue
        if any(t in target_node for t in targets):
            try:
                path = nx.shortest_path(G, source=start_node, target=target_node)
                attack_paths.append(path)
            except nx.NetworkXNoPath:
                continue

    if attack_paths:
        print(f"[+] {len(attack_paths)} attack paths found:\n")
        with open("attack_paths_report.txt", "w") as f:
            for path in attack_paths:
                risk = score_path(path)
                formatted = f"RISK [{risk}/40]: " + " → ".join(path)
                print(formatted)
                f.write(formatted + "\n")

        print("\n[✓] Attack paths saved to 'attack_paths_report.txt'\n")
    else:
        print("[!] No reachable targets from this node.")

# ----------- ENTRY POINT -----------
if __name__ == "__main__":
    print("\n=== Predictive Posture Analyst: Attack Path Simulator ===\n")
    print("Example start nodes: user:apache, process:nginx, user:flowjav\n")
    user_input = input("Enter start node: ").strip()
    simulate_attack_paths(user_input)

