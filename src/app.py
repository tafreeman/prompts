from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import re
import os

app = Flask(__name__)

# Database configuration
DATABASE = 'prompt_library.db'


def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with required tables.

    This uses the same schema as `load_prompts.py` to avoid drift between
    the web app and the ingestion script. If you change the schema here,
    make the same change in `load_prompts.load_expanded_prompts`.
    """
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS prompts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        persona TEXT NOT NULL,
        use_case TEXT,
        category TEXT NOT NULL,
        platform TEXT NOT NULL,
        template TEXT NOT NULL,
        description TEXT,
        tags TEXT,
        created_date TEXT,
        usage_count INTEGER DEFAULT 0,
        difficulty TEXT,
        governance_tags TEXT,
        data_classification TEXT,
        risk_level TEXT,
        regulatory_scope TEXT,
        approval_required TEXT,
        retention_period TEXT
    )''')
    conn.commit()
    conn.close()


def extract_placeholders(template):
    """Extract placeholders from prompt template"""
    placeholders = re.findall(r'\[([^\]]+)\]', template)
    return list(set(placeholders))


def update_usage_count(prompt_id):
    """Update usage count for a prompt"""
    conn = get_db_connection()
    conn.execute('UPDATE prompts SET usage_count = usage_count + 1 WHERE id = ?', (prompt_id,))
    conn.commit()
    conn.close()


@app.route('/')
def index():
    """Main library page with search and filtering"""
    conn = get_db_connection()

    # Get filter parameters
    persona_filter = request.args.get('persona', '')
    category_filter = request.args.get('category', '')
    platform_filter = request.args.get('platform', '')
    search_query = request.args.get('search', '')
    # Governance filters
    risk_level_filter = request.args.get('risk_level', '')
    data_classification_filter = request.args.get('data_classification', '')
    approval_required_filter = request.args.get('approval_required', '')

    # Build query with filters
    query = 'SELECT * FROM prompts WHERE 1=1'
    params = []

    if persona_filter:
        query += ' AND persona = ?'
        params.append(persona_filter)

    if category_filter:
        query += ' AND category = ?'
        params.append(category_filter)

    if platform_filter:
        query += ' AND platform = ?'
        params.append(platform_filter)

    if search_query:
        query += ' AND (title LIKE ? OR description LIKE ? OR tags LIKE ?)'
        search_param = f'%{search_query}%'
        params.extend([search_param, search_param, search_param])

    # Governance filters
    if risk_level_filter:
        query += ' AND risk_level = ?'
        params.append(risk_level_filter)

    if data_classification_filter:
        query += ' AND data_classification = ?'
        params.append(data_classification_filter)

    if approval_required_filter:
        query += ' AND approval_required = ?'
        params.append(approval_required_filter)

    query += ' ORDER BY title'

    prompts = conn.execute(query, params).fetchall()

    # Get filter options
    personas = conn.execute('SELECT DISTINCT persona FROM prompts ORDER BY persona').fetchall()
    categories = conn.execute('SELECT DISTINCT category FROM prompts ORDER BY category').fetchall()
    platforms = conn.execute('SELECT DISTINCT platform FROM prompts ORDER BY platform').fetchall()
    # Governance filter options
    risk_levels = conn.execute(
        'SELECT DISTINCT risk_level FROM prompts WHERE risk_level IS NOT NULL '
        'AND risk_level != "" ORDER BY risk_level').fetchall()
    data_classifications = conn.execute(
        'SELECT DISTINCT data_classification FROM prompts '
        'WHERE data_classification IS NOT NULL AND data_classification != "" '
        'ORDER BY data_classification').fetchall()
    approval_required_options = conn.execute(
        'SELECT DISTINCT approval_required FROM prompts '
        'WHERE approval_required IS NOT NULL AND approval_required != "" '
        'ORDER BY approval_required').fetchall()

    conn.close()

    return render_template('index.html',
                           prompts=prompts,
                           personas=personas,
                           categories=categories,
                           platforms=platforms,
                           risk_levels=risk_levels,
                           data_classifications=data_classifications,
                           approval_required_options=approval_required_options,
                           current_filters={
                               'persona': persona_filter,
                               'category': category_filter,
                               'platform': platform_filter,
                               'search': search_query,
                               'risk_level': risk_level_filter,
                               'data_classification': data_classification_filter,
                               'approval_required': approval_required_filter
                           })


@app.route('/prompt/<int:prompt_id>')
def prompt_detail(prompt_id):
    """Detailed view of a specific prompt"""
    conn = get_db_connection()
    prompt = conn.execute('SELECT * FROM prompts WHERE id = ?', (prompt_id,)).fetchone()
    conn.close()

    if prompt is None:
        return redirect(url_for('index'))

    placeholders = extract_placeholders(prompt['template'])

    return render_template('prompt_detail.html', prompt=prompt, placeholders=placeholders)


@app.route('/customize/<int:prompt_id>')
def customize_prompt(prompt_id):
    """Prompt customization page with dynamic form"""
    conn = get_db_connection()
    prompt = conn.execute('SELECT * FROM prompts WHERE id = ?', (prompt_id,)).fetchone()
    conn.close()

    if prompt is None:
        return redirect(url_for('index'))

    placeholders = extract_placeholders(prompt['template'])

    return render_template('customize.html', prompt=prompt, placeholders=placeholders)


@app.route('/api/customize', methods=['POST'])
def api_customize():
    """API endpoint for prompt customization"""
    data = request.get_json()
    prompt_id = data.get('prompt_id')
    replacements = data.get('replacements', {})

    conn = get_db_connection()
    prompt = conn.execute('SELECT * FROM prompts WHERE id = ?', (prompt_id,)).fetchone()
    conn.close()

    if prompt is None:
        return jsonify({'error': 'Prompt not found'}), 404

    # Replace placeholders in template
    customized_template = prompt['template']
    for placeholder, value in replacements.items():
        customized_template = customized_template.replace(f'[{placeholder}]', value)

    # Update usage count
    update_usage_count(prompt_id)

    return jsonify({
        'customized_prompt': customized_template,
        'original_template': prompt['template']
    })


@app.route('/analytics')
def analytics():
    """Analytics dashboard with usage statistics"""
    conn = get_db_connection()

    # Get overall statistics
    total_prompts = conn.execute('SELECT COUNT(*) as count FROM prompts').fetchone()['count']
    total_usage = conn.execute('SELECT SUM(usage_count) as total FROM prompts').fetchone()['total'] or 0

    # Get top used prompts
    top_prompts = conn.execute('''
        SELECT title, usage_count, persona, platform
        FROM prompts
        WHERE usage_count > 0
        ORDER BY usage_count DESC
        LIMIT 10
    ''').fetchall()

    # Get usage by persona
    persona_stats = conn.execute('''
        SELECT persona, COUNT(*) as count, SUM(usage_count) as usage
        FROM prompts
        GROUP BY persona
        ORDER BY usage DESC
    ''').fetchall()

    # Get usage by platform
    platform_stats = conn.execute('''
        SELECT platform, COUNT(*) as count, SUM(usage_count) as usage
        FROM prompts
        GROUP BY platform
        ORDER BY usage DESC
    ''').fetchall()

    # Get usage by category
    category_stats = conn.execute('''
        SELECT category, COUNT(*) as count, SUM(usage_count) as usage
        FROM prompts
        GROUP BY category
        ORDER BY usage DESC
    ''').fetchall()

    # Get governance statistics
    risk_level_stats = conn.execute('''
        SELECT risk_level, COUNT(*) as count
        FROM prompts
        WHERE risk_level IS NOT NULL AND risk_level != ""
        GROUP BY risk_level
        ORDER BY
            CASE risk_level
                WHEN 'Low' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'High' THEN 3
                WHEN 'Critical' THEN 4
                ELSE 5
            END
    ''').fetchall()

    data_classification_stats = conn.execute('''
        SELECT data_classification, COUNT(*) as count
        FROM prompts
        WHERE data_classification IS NOT NULL AND data_classification != ""
        GROUP BY data_classification
        ORDER BY count DESC
    ''').fetchall()

    approval_required_stats = conn.execute('''
        SELECT approval_required, COUNT(*) as count
        FROM prompts
        WHERE approval_required IS NOT NULL AND approval_required != ""
        GROUP BY approval_required
        ORDER BY count DESC
    ''').fetchall()

    # Count prompts with governance metadata
    governance_count = conn.execute('''
        SELECT COUNT(*) as count FROM prompts
        WHERE (governance_tags IS NOT NULL AND governance_tags != "")
           OR (risk_level IS NOT NULL AND risk_level != "")
    ''').fetchone()['count']

    conn.close()

    return render_template('analytics.html',
                           total_prompts=total_prompts,
                           total_usage=total_usage,
                           top_prompts=top_prompts,
                           persona_stats=persona_stats,
                           platform_stats=platform_stats,
                           category_stats=category_stats,
                           risk_level_stats=risk_level_stats,
                           data_classification_stats=data_classification_stats,
                           approval_required_stats=approval_required_stats,
                           governance_count=governance_count)


@app.route('/api/search')
def api_search():
    """API endpoint for search functionality"""
    query = request.args.get('q', '')
    persona = request.args.get('persona', '')
    category = request.args.get('category', '')
    platform = request.args.get('platform', '')

    conn = get_db_connection()

    sql_query = 'SELECT * FROM prompts WHERE 1=1'
    params = []

    if query:
        sql_query += ' AND (title LIKE ? OR description LIKE ? OR tags LIKE ?)'
        search_param = f'%{query}%'
        params.extend([search_param, search_param, search_param])

    if persona:
        sql_query += ' AND persona = ?'
        params.append(persona)

    if category:
        sql_query += ' AND category = ?'
        params.append(category)

    if platform:
        sql_query += ' AND platform = ?'
        params.append(platform)

    sql_query += ' ORDER BY title'

    results = conn.execute(sql_query, params).fetchall()
    conn.close()

    return jsonify([dict(row) for row in results])


if __name__ == '__main__':
    init_db()
    # Only enable debug mode if explicitly set via environment variable
    # Never use debug=True in production!
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
