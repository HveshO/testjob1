from flask import Flask, request, render_template,jsonify
from tinydb import TinyDB
import re
import datetime
import requests
app = Flask(__name__)

db = TinyDB('database.json')

def validate_fields(fields):
    for field_name, field_value in fields.items():
        # можно было бы использовать, но месяц может быть 91 к примеру
        # if re.compile(r'\d{4}-\d{2}-\d{2}').match(field_value):
        BOOL_DATE = False
        try:
            datetime.datetime.strptime(field_value, "%d.%m.%Y")
            BOOL_DATE = True
        except ValueError:
            try:
                datetime.datetime.strptime(field_value, "%Y-%m-%d")
                BOOL_DATE = True
            except ValueError:
                pass
        if BOOL_DATE:
            fields[field_name] = 'date'
            continue
        elif re.compile(r'^\+7 \d{3} \d{3} \d{2} \d{2}$').match(field_value)\
                or re.compile(r'^\+7\d{3}\d{3}\d{2}\d{2}$').match(field_value):
            fields[field_name] = 'phone'
            continue
        elif re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$').match(field_value):
            fields[field_name] = 'email'
            continue
        else:
            fields[field_name] = 'text'
    return fields

@app.route('/get_form', methods=['GET'])
def index():
    response = requests.post('http://localhost:5000/get_form', params=request.args)
    return response.text


@app.route('/get_form', methods=['POST'])
def get_form():
    # параметры в post запрос передаются через body
    # но тз есть тз
    data = request.args.to_dict()
    #print(data)
    data_type = validate_fields(data)
    names = []
    for template in db:
        template_fields = {k: v for k, v in template.items() if k != "name"}
        if not template_fields:
            continue
        if (set(template_fields.items())).issubset(set(data_type.items())):
            names.append(template["name"])
    if len(names) > 0:
        if len(names)==1:
            return jsonify(names[0])
        else:
            return jsonify(names)
    else:
        return jsonify(data_type)


if __name__ == '__main__':
    app.run(debug=True)
