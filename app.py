"""Flask web application for the autonomous research assistant."""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import threading
import json
from datetime import datetime
from research_assistant import AutonomousResearchAssistant
from config import Config
import traceback

app = Flask(__name__)
CORS(app)

# Global state for running research tasks
research_tasks = {}
task_lock = threading.Lock()

def run_research_task(task_id, domain=None):
    """Run research in background thread."""
    try:
        assistant = AutonomousResearchAssistant()
        report = assistant.run_autonomous_research(domain=domain)
        
        # Get report file path
        report_files = [f for f in os.listdir(Config.REPORTS_DIR) 
                       if f.endswith('.md')]
        latest_report = max(report_files, key=lambda f: os.path.getmtime(
            os.path.join(Config.REPORTS_DIR, f))) if report_files else None
        
        with task_lock:
            research_tasks[task_id]['status'] = 'completed'
            research_tasks[task_id]['report'] = report
            research_tasks[task_id]['report_file'] = latest_report
            research_tasks[task_id]['completed_at'] = datetime.now().isoformat()
            
    except Exception as e:
        with task_lock:
            research_tasks[task_id]['status'] = 'error'
            research_tasks[task_id]['error'] = str(e)
            research_tasks[task_id]['error_traceback'] = traceback.format_exc()
            research_tasks[task_id]['completed_at'] = datetime.now().isoformat()

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    try:
        Config.validate()
        return jsonify({
            'status': 'healthy',
            'api_configured': bool(Config.GOOGLE_API_KEY)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/research/start', methods=['POST'])
def start_research():
    """Start a new research task."""
    try:
        data = request.get_json() or {}
        domain = data.get('domain', None)
        
        # Generate task ID
        task_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Initialize task
        with task_lock:
            research_tasks[task_id] = {
                'task_id': task_id,
                'domain': domain or 'auto-selected',
                'status': 'running',
                'started_at': datetime.now().isoformat(),
                'progress': 'Initializing...'
            }
        
        # Start research in background thread
        thread = threading.Thread(
            target=run_research_task,
            args=(task_id, domain),
            daemon=True
        )
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'status': 'started',
            'message': 'Research task started'
        }), 202
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/research/status/<task_id>', methods=['GET'])
def get_research_status(task_id):
    """Get status of a research task."""
    with task_lock:
        task = research_tasks.get(task_id)
    
    if not task:
        return jsonify({
            'error': 'Task not found'
        }), 404
    
    response = {
        'task_id': task_id,
        'status': task['status'],
        'domain': task.get('domain'),
        'started_at': task.get('started_at'),
        'completed_at': task.get('completed_at'),
        'progress': task.get('progress', 'Unknown')
    }
    
    if task['status'] == 'completed':
        response['report_file'] = task.get('report_file')
        # Include preview of report
        if 'report' in task:
            response['report_preview'] = task['report'][:1000] + '...' if len(task['report']) > 1000 else task['report']
    
    if task['status'] == 'error':
        response['error'] = task.get('error')
    
    return jsonify(response), 200

@app.route('/api/research/report/<task_id>', methods=['GET'])
def get_research_report(task_id):
    """Get the full research report."""
    with task_lock:
        task = research_tasks.get(task_id)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    if task['status'] != 'completed':
        return jsonify({
            'error': 'Research not completed yet',
            'status': task['status']
        }), 400
    
    # Try to return report file if available
    report_file = task.get('report_file')
    if report_file:
        report_path = os.path.join(Config.REPORTS_DIR, report_file)
        if os.path.exists(report_path):
            return send_file(
                report_path,
                mimetype='text/markdown',
                as_attachment=True,
                download_name=report_file
            )
    
    # Fallback to stored report
    if 'report' in task:
        return jsonify({
            'report': task['report'],
            'format': 'markdown'
        }), 200
    
    return jsonify({'error': 'Report not available'}), 404

@app.route('/api/research/list', methods=['GET'])
def list_research_tasks():
    """List all research tasks."""
    with task_lock:
        tasks = list(research_tasks.values())
    
    # Sort by started_at (most recent first)
    tasks.sort(key=lambda x: x.get('started_at', ''), reverse=True)
    
    return jsonify({
        'tasks': tasks,
        'count': len(tasks)
    }), 200

@app.route('/api/research/cancel/<task_id>', methods=['POST'])
def cancel_research(task_id):
    """Cancel a research task (if possible)."""
    with task_lock:
        task = research_tasks.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        if task['status'] == 'completed':
            return jsonify({'error': 'Task already completed'}), 400
        
        task['status'] = 'cancelled'
        task['cancelled_at'] = datetime.now().isoformat()
    
    return jsonify({
        'task_id': task_id,
        'status': 'cancelled'
    }), 200

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    os.makedirs(Config.VISUALIZATIONS_DIR, exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

