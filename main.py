from flask import Flask, request, jsonify
from dbFuctions import generate_quiz_with_answers, get_course_notes

app = Flask(__name__)

@app.route("/generate_quiz", methods=["POST"])
def generate_quiz():
    try:
        # Extract Firebase ref from request
        data = request.json
        firebase_ref = data["firebase_ref"]

        # Step 1: Get notes
        notes = get_course_notes(firebase_ref)

        # Step 2: Generate quiz
        raw_quiz_data = generate_quiz_with_answers(notes)

        # Step 3: Format JSON
        quiz_json = raw_quiz_data

        return jsonify({"success": True, "quiz": quiz_json}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
