from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS prompts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT,
                  persona TEXT NOT NULL,
                  category TEXT NOT NULL,
                  prompt_text TEXT NOT NULL,
                  variables TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS usage_stats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  prompt_id INTEGER,
                  used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  customizations TEXT,
                  FOREIGN KEY (prompt_id) REFERENCES prompts (id))''')
    
    # Insert basic sample data
    sample_prompts = [
        ("Code Review Assistant", "Helps review code for best practices", "Developer", "Code Quality", 
         "Please review the following code for:\n1. Best practices\n2. Security vulnerabilities\n3. Performance issues\n4. Code maintainability\n\nCode to review:\n{code}\n\nPlease provide specific feedback and suggestions for improvement.", 
         '["code"]'),
        ("Project Charter Template", "Creates comprehensive project charters", "Project Manager", "Planning", 
         "Create a project charter for:\n\nProject Name: {project_name}\nBusiness Objective: {objective}\nKey Stakeholders: {stakeholders}\n\nInclude:\n- Executive Summary\n- Scope and Deliverables\n- Timeline and Milestones\n- Resource Requirements\n- Risk Assessment", 
         '["project_name", "objective", "stakeholders"]'),
        ("System Architecture Review", "Reviews system architecture designs", "Architect", "Design", 
         "Review the following system architecture for:\n\nSystem: {system_name}\nRequirements: {requirements}\n\nEvaluate:\n1. Scalability\n2. Security\n3. Maintainability\n4. Performance\n5. Cost-effectiveness\n\nProvide recommendations for improvement.", 
         '["system_name", "requirements"]')
    ]
    
    for prompt in sample_prompts:
        c.execute("INSERT OR IGNORE INTO prompts (title, description, persona, category, prompt_text, variables) VALUES (?, ?, ?, ?, ?, ?)", prompt)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    
    # Get filter parameters
    persona_filter = request.args.get('persona', '')
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    # Build query
    query = "SELECT * FROM prompts WHERE 1=1"
    params = []
    
    if persona_filter:
        query += " AND persona = ?"
        params.append(persona_filter)
    
    if category_filter:
        query += " AND category = ?"
        params.append(category_filter)
    
    if search_query:
        query += " AND (title LIKE ? OR description LIKE ? OR prompt_text LIKE ?)"
        search_param = f"%{search_query}%"
        params.extend([search_param, search_param, search_param])
    
    c.execute(query, params)
    prompts = c.fetchall()
    
    # Get unique personas and categories for filters
    c.execute("SELECT DISTINCT persona FROM prompts ORDER BY persona")
    personas = [row[0] for row in c.fetchall()]
    
    c.execute("SELECT DISTINCT category FROM prompts ORDER BY category")
    categories = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    return render_template('index.html', prompts=prompts, personas=personas, categories=categories,
                         current_persona=persona_filter, current_category=category_filter, 
                         current_search=search_query)

@app.route('/prompt/<int:prompt_id>')
def view_prompt(prompt_id):
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    prompt = c.fetchone()
    conn.close()
    
    if not prompt:
        return redirect(url_for('index'))
    
    return render_template('prompt_detail.html', prompt=prompt)

@app.route('/customize/<int:prompt_id>', methods=['POST'])
def customize_prompt(prompt_id):
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM prompts WHERE id = ?", (prompt_id,))
    prompt = c.fetchone()
    
    if not prompt:
        return jsonify({'error': 'Prompt not found'}), 404
    
    # Get customization data
    customizations = request.json
    
    # Replace variables in prompt text
    customized_text = prompt[5]  # prompt_text is at index 5
    for key, value in customizations.items():
        customized_text = customized_text.replace(f"{{{key}}}", value)
    
    # Log usage
    c.execute("INSERT INTO usage_stats (prompt_id, customizations) VALUES (?, ?)", 
              (prompt_id, json.dumps(customizations)))
    conn.commit()
    conn.close()
    
    return jsonify({'customized_prompt': customized_text})

@app.route('/analytics')
def analytics():
    conn = sqlite3.connect('prompt_library.db')
    c = conn.cursor()
    
    # Get usage statistics
    c.execute("""SELECT p.persona, COUNT(u.id) as usage_count 
                 FROM prompts p 
                 LEFT JOIN usage_stats u ON p.id = u.prompt_id 
                 GROUP BY p.persona 
                 ORDER BY usage_count DESC""")
    persona_stats = c.fetchall()
    
    c.execute("""SELECT p.title, COUNT(u.id) as usage_count 
                 FROM prompts p 
                 LEFT JOIN usage_stats u ON p.id = u.prompt_id 
                 GROUP BY p.id, p.title 
                 ORDER BY usage_count DESC 
                 LIMIT 10""")
    popular_prompts = c.fetchall()
    
    c.execute("SELECT COUNT(*) FROM prompts")
    total_prompts = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM usage_stats")
    total_usage = c.fetchone()[0]
    
    conn.close()
    
    return render_template('analytics.html', 
                         persona_stats=persona_stats,
                         popular_prompts=popular_prompts,
                         total_prompts=total_prompts,
                         total_usage=total_usage)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)