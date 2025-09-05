import pandas as pd
from flask import Flask,render_template,jsonify,request,json

data_location = "dating_app/data/okcupid_profiles.csv"
df = pd.read_csv(data_location)

user = {
    "age": 19,
    "status": 'single',
    "sex": 'm',
    "orientation": 'straight',
    "body_type": 'average',
    "diet": 'mostly anything',
    "drinks": 'socially',
    "drugs": 'never',
    "education": 'graduated from college/university',
    "ethnicity": 'white',
    "height": 65.0,
    "income": -1,
    "job": 'student',
    "location": 'san fransisco, california',
    "offspring": "doesn't have kids",
    "pets": 'has dogs and likes cats',
    "religion": 'catholicism',
    "sign": 'taurus',
    "smokes": 'no',
    "language": 'english'
}

multipliers = {
    "age": 0,
    "status": 0,
    "sex": 0,
    "orientation": 0,
    "body_type": 0,
    "diet": 25,
    "drinks": 50,
    "drugs": 0,
    "education": 20,
    "ethnicity": 0,
    "height": 0,
    "income": 0,
    "job": 0,
    "location": 80,
    "offspring": 0,
    "pets": 60,
    "religion": 15,
    "sign": 30,
    "smokes": 90,
    "language": 0
}

app = Flask(__name__)

@app.route("/")
def load_main_page():
    return render_template('index.html')

@app.route("/match")
def do_matching():
    new_match = match_person(user)
    print(new_match)
    match_dict = {
        "age": int(new_match['age']),
        "status": str(new_match['status']),
        "sex": str(new_match['sex']),
        "orientation": str(new_match['orientation']),
        "body_type": str(new_match['body_type']),
        "diet": str(new_match['diet']),
        "drinks": str(new_match['drinks']),
        "drugs": str(new_match['drugs']),
        "education": str(new_match['education']),
        "ethnicity": str(new_match['ethnicity']),
        "height": float(new_match['height']),
        "income": float(new_match['income']),
        "job": str(new_match['job']),
        "location": str(new_match['location']),
        "offspring": str(new_match['offspring']),
        "pets": str(new_match['pets']),
        "religion": str(new_match['religion']),
        "sign": str(new_match['sign']),
        "smokes": str(new_match['smokes']),
    }
    print(match_dict)
    return jsonify(match_dict)

@app.route("/submit")
def submit_preferences():
    print(request.args.get('pets'))
    multipliers['diet'] = int(request.args.get('diet'))
    multipliers['drink'] = int(request.args.get('drink'))
    multipliers['smoke'] = int(request.args.get('smoke'))
    multipliers['education'] = int(request.args.get('education'))
    multipliers['location'] = int(request.args.get('location'))
    multipliers['religion'] = int(request.args.get('religion'))
    multipliers['starsign'] = int(request.args.get('starsign'))
    multipliers['pets'] = int(request.args.get('pets'))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def get_match_score(user, person):
    score = 0
    for key in user:
        if key not in person:
            continue

        if user[key] == person[key]:
            score += 1 * multipliers[key]
        
    user_min_age = (user['age'] / 2) + 7
    person_min_age = (person['age'] / 2) + 7

    if user['age'] < person_min_age or person['age'] < user_min_age: #age mismatch
        return -10000
    if user['orientation'] == 'straight' and person['sex'] == user['sex']: #straight check
        return -10000
    if user['orientation'] == 'gay' and person['sex'] != user['sex']: #gay check
        return -10000
    if person['orientation'] == 'straight' and person['sex'] == user['sex']:
        return -10000
    if person['orientation'] == 'gay' and person['sex'] != user['sex']:
        return -10000
    user_loc = user['location'].split(", ")
    person_loc = person['location'].split(", ")
    if user_loc[1] != person_loc[1]: #not in the same state
        return -10000
    

    return score

def match_person(user):
    best_index = 0
    best_score = 0

    for index, row in df.iterrows():
        person = row.to_dict() 
        score = get_match_score(user, person)
        if score > best_score:
            best_index = index
            best_score = score

    return df.loc[best_index]

def match_people(user):
    list_people = [] #A list of people by index and score
    for index, row in df.iterrows():
        person = row.to_dict()
        score = get_match_score(user, person)
        list_people.append([score, index])
    
    list_people.sort(reverse=True)
    return list_people


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)