from flask import Flask, request, jsonify
from flask_cors import CORS
from dbFuctions import generate_quiz_with_answers, get_course_notes

app = Flask(__name__)
cors = CORS(app)

test2_file = "notes/neralNetworks.docx"

@app.route("/generate_quiz", methods=["POST"])
def generate_quiz():
    try:
        # Extract Firebase ref from request
        data = request.json
        firebase_ref = data["firebase_ref"]

        # Get notes
        notes = get_course_notes(firebase_ref)

        # Generate quiz
        raw_quiz_data = generate_quiz_with_answers(notes)

        # Format JSON
        quiz_json = raw_quiz_data

        return jsonify({"success": True, "quiz": quiz_json}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route("/transcribe_video", methods=["POST"])
def transcribe_video():
    pass

if __name__ == "__main__":
    app.run(debug=True,host="localhost",port="3080")
