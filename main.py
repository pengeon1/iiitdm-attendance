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
    
    if not roll_no:
        return jsonify({"error": "Missing roll number parameter"}), 400

    url = f"https://mis.iiitdm.ac.in/Profile/automation/ajax/ajax.php?method=StudSubject123&RegTable=reg_jul_nov_2024&StudentID={roll_no}"

    try:
        # Adding headers to mimic a browser request to prevent potential blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        # Make the request
        req = requests.get(url, headers=headers, timeout=10)
        req.raise_for_status()  # Raise an error for bad HTTP status codes
        
        soup = BeautifulSoup(req.text, "html.parser")

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
        error_message = f"Failed to fetch data from the server: {e}"
        print(f"Error: {error_message}")
        return jsonify({"error": error_message}), 500

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(f"Unexpected Error: {error_message}")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
