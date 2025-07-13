import json
import networkx as nx
import matplotlib.pyplot as plt

# Load structured data
with open("normalized_output.json") as f:
    data = json.load(f)

G = nx.DiGraph()

# ---------- Add Nodes ----------
# Users
for user in data.get("users", []):
    G.add_node(f"user:{user['username']}", type="user")

# Groups
for group, members in data.get("groups", {}).items():
    G.add_node(f"group:{group}", type="group")
    for member in members:
        G.add_edge(f"user:{member}", f"group:{group}", relation="member_of")

# Processes
for proc in data.get("running_processes", []):
    G.add_node(f"process:{proc['command']}", type="process")
    G.add_edge(f"user:{proc['user']}", f"process:{proc['command']}", relation="runs")

# Services
for svc in data.get("services", []):
    G.add_node(f"service:{svc}", type="service")

# Ports
for port in data.get("open_ports", []):
    G.add_node(f"port:{port}", type="port")
    if "sshd" in port:
        G.add_edge("service:sshd", f"port:{port}", relation="listens_on")
    if "nginx" in port:
        G.add_edge("service:nginx", f"port:{port}", relation="listens_on")

# Sudo privileges
for entry in data.get("sudo_privileges", []):
    if ":" in entry:
        user = entry.split(":")[0]
        G.add_edge(f"user:{user}", "user:root", relation="can_sudo")

# Firewall Rules
for rule in data.get("firewall_rules", []):
    G.add_node(f"firewall_rule:{rule}", type="firewall_rule")

# Crontabs (persistence risks)
for line in data.get("cronjobs", []):
    G.add_node(f"cronjob:{line}", type="cron")
    G.add_edge("user:root", f"cronjob:{line}", relation="executes_on_schedule")

# ---------- Visualize ----------
print(f"\n[+] Total Nodes: {len(G.nodes())}")


print(f"[+] Total Edges: {len(G.edges())}")

def build_graph():
    return G

pos = nx.spring_layout(G, k=0.5)

node_colors = []
for n in G.nodes():
    if "user:" in n:
        node_colors.append("lightblue")
    elif "process:" in n:
        node_colors.append("lightgreen")
    elif "port:" in n:
        node_colors.append("orange")
    elif "service:" in n:
        node_colors.append("violet")
    else:
        node_colors.append("gray")

plt.figure(figsize=(14, 10))
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_size=8, arrows=True)
edge_labels = nx.get_edge_attributes(G, 'relation')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
plt.title("PPA Risk Graph - System Relationships")
plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
plt.savefig("ppa_graph_output.png", dpi=300)
plt.show()

