from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('attendance.html')

@app.route('/attendance', methods=['GET'])
def fetch_attendance():
    roll_no = request.args.get('roll_no')

    if not roll_no:
        return jsonify({"error": "Missing roll number parameter"}), 400

    url = f"https://mis.iiitdm.ac.in/Profile/automation/ajax/ajax.php?method=StudSubject123&RegTable=reg_jul_nov_2024&StudentID={roll_no}"

    try:
        req = requests.get(url)
        req.raise_for_status()  # Raises HTTPError if the HTTP request returned an unsuccessful status code

        soup = BeautifulSoup(req.text, "html.parser")

        # Extract table rows
        all_subs = []
        for row in soup.find_all('tr'):
            cols = row.find_all('td')
            if cols:  # Skip empty rows
                subject = {
                    "sno": cols[0].text.strip(),
                    "course_id": cols[1].text.strip(),
                    "course_name": cols[2].text.strip(),
                    "faculty_name": cols[3].text.strip(),
                    "total": cols[4].text.strip(),
                    "present": cols[5].text.strip(),
                    "absent": cols[6].text.strip(),
                    "no_class": cols[7].text.strip(),
                    "provisional_approved_leave": cols[8].text.strip(),
                    "present_percentage": cols[9].text.strip(),
                    "absent_percentage": cols[10].text.strip(),
                    "approved_leave_percentage": cols[11].text.strip(),
                    "percentage": cols[12].text.strip()
                }
                all_subs.append(subject)

        return jsonify(all_subs)

    except requests.exceptions.RequestException as e:
        # Catch HTTP request errors
        error_message = f"Failed to fetch data from the server: {e}"
        print(error_message)  # This will show in Vercel logs
        return jsonify({"error": error_message}), 500

    except Exception as e:
        # Catch any other general exceptions
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)  # This will show in Vercel logs
        print(traceback.format_exc())  # Print stack trace for better debugging
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
