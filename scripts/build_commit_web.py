import urllib.request
import json
import os
import math
from datetime import datetime, timedelta

def build_commit_web():
    # 1. Fetch public repos for Aryanshettar007
    username = "Aryanshettar007"
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            repos = json.loads(response.read().decode())
    except Exception as e:
        print(f"Failed to fetch repos: {e}")
        repos = []

    # Filter out empty or non-code repos
    active_repos = [r for r in repos if not r['fork']][:8]
    
    if not active_repos:
        print("No active repos found.")
        return

    width = 800
    height = 500
    cx = width / 2
    cy = height / 2
    max_radius = 200

    svg_elements = []
    
    svg_elements.append('''
    <style>
        .commit-line {
            fill: none;
            stroke-linecap: round;
            animation: pulse 3s infinite alternate;
        }
        .repo-node {
            fill: #E23636;
            stroke: #0d1117;
            stroke-width: 2;
        }
        .repo-text {
            font-family: monospace;
            font-size: 14px;
            fill: #c9d1d9;
            text-anchor: middle;
        }
        @keyframes pulse {
            0% { filter: drop-shadow(0 0 2px #E23636); opacity: 0.7; }
            100% { filter: drop-shadow(0 0 10px #E23636); opacity: 1; }
        }
    </style>
    ''')

    # Central Node (The User)
    svg_elements.append(f'<circle cx="{cx}" cy="{cy}" r="15" fill="#1F3A93" />')
    svg_elements.append(f'<text x="{cx}" y="{cy+5}" font-family="monospace" font-weight="bold" font-size="12" fill="white" text-anchor="middle">ME</text>')

    num_repos = len(active_repos)
    for i, repo in enumerate(active_repos):
        name = repo['name']
        stars = repo['stargazers_count']
        
        # Calculate angle
        angle = (i / num_repos) * 2 * math.pi
        
        # Distance based on stars (more stars = closer to center, as a fun metric)
        # But for layout, we keep it fixed radius or semi-fixed
        radius = max_radius - (stars * 2)
        if radius < 80: radius = 80
        
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        
        # Line connecting to center
        # Thickness based on recent activity (mocked here based on size/stars for simplicity)
        thickness = 1 + min(stars, 5)
        
        svg_elements.append(f'<line class="commit-line" x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#E23636" stroke-width="{thickness}" />')
        
        # Repo Node
        node_radius = 8 + min(stars, 10)
        svg_elements.append(f'<circle class="repo-node" cx="{x}" cy="{y}" r="{node_radius}" />')
        
        # Text label
        label_y = y - node_radius - 8 if y < cy else y + node_radius + 15
        svg_elements.append(f'<text class="repo-text" x="{x}" y="{label_y}">{name}</text>')
        
        # Connect to next node to form the "web"
        next_i = (i + 1) % num_repos
        next_angle = (next_i / num_repos) * 2 * math.pi
        next_radius = max_radius - (active_repos[next_i]['stargazers_count'] * 2)
        if next_radius < 80: next_radius = 80
        
        nx = cx + next_radius * math.cos(next_angle)
        ny = cy + next_radius * math.sin(next_angle)
        
        svg_elements.append(f'<line x1="{x}" y1="{y}" x2="{nx}" y2="{ny}" stroke="rgba(255, 255, 255, 0.1)" stroke-width="1" stroke-dasharray="5,5" />')


    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%">
    <rect width="{width}" height="{height}" fill="#0d1117" rx="10"/>
    ''' + "\n".join(svg_elements) + "\n</svg>"

    os.makedirs("assets", exist_ok=True)
    output_path = os.path.join("assets", "commit-web.svg")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated Live Commit Web at {output_path}")

if __name__ == "__main__":
    build_commit_web()
