from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('attendance.html')

@app.route('/attendance', methods=['GET'])
def fetch_attendance():
    roll_no = request.args.get('roll_no')

    # Replace with the actual URL you use for scraping
    url = f"https://mis.iiitdm.ac.in/Profile/automation/ajax/ajax.php?method=StudSubject123&RegTable=reg_jul_nov_2024&StudentID={roll_no}"

    try:
        req = requests.get(url)
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

    except Exception as e:
        return jsonify({"error": "Failed to fetch attendance data.", "details": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
