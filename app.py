from flask import Flask, jsonify
import subprocess
import os
import sys

main_app = Flask(__name__)

def start_sub_app(directory, script, port):
    """Starts a sub-application as a separate process."""
    # Path to the virtual environment's Python executable
    venv_python = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
    script_path = os.path.join(os.getcwd(), directory, script)

    # Set environment variables to prevent Flask auto-reload conflicts
    env = os.environ.copy()
    env["FLASK_ENV"] = "production"
    env["WERKZEUG_RUN_MAIN"] = "true"
    env.pop("FLASK_DEBUG", None)

    try:
        # Start the sub-app in a separate process and log the output
        process = subprocess.Popen([venv_python, script_path], cwd=os.getcwd(), env=env, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        print(f"Started {script} on port {port}")

        # Log any output or error from the process
        stdout, stderr = process.communicate()
        if stdout:
            print(f"Output from {script}:\n{stdout.decode()}")
        if stderr:
            print(f"Error from {script}:\n{stderr.decode()}", file=sys.stderr)

    except Exception as e:
        print(f"Error starting {script}: {e}", file=sys.stderr)

@main_app.route('/')
def home():
    return jsonify({"message": "Main Flask App - Running!"})

@main_app.route('/status')
def status():
    return jsonify({
        "status": "Main app running",
        "sub_apps": ["shortage", "demand", "overstock"]
    })

if __name__ == "__main__":
    # Start the sub-apps
    start_sub_app("shortage", "shortage_app.py", 5002)  # Shortage component

    # Run the main app
    main_app.run(host="127.0.0.1", port=5000, debug=False)
