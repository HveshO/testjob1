from flask import Flask, request, render_template
from tinydb import TinyDB
import re
import datetime
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
        print(BOOL_DATE, re.compile(
            r'^\+7 \d{3} \d{3} \d{2} \d{2}$').match(field_value))
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


def transdata(original_dict):
    return {original_dict[f'f_name{i}']: original_dict[f'value{i}'] for i in range(1, len(original_dict)//2 + 1)}


@app.route('/get_form', methods=['GET'])
def index():
    return render_template('index.html', amount=2)


@app.route('/get_form', methods=['POST'])
def get_form(
    # field_names: list[str]
):
    #url_params = dict(request.args)
    #print(dict(url_params))
    data = request.form.to_dict()
    data = transdata(data)
    data_type = validate_fields(data)
    names = []
    for template in db:
        template_fields = {k: v for k, v in template.items() if k != "name"}
        if not template_fields:
            continue
        if (set(template_fields.items())).issubset(set(data_type.items())):
            names.append(template["name"])
    amount = len(request.form.to_dict())//2
    if len(names) > 0:
        data = {
            'data': data,
            'bool': True,
            'content': names
        }
        #return jsonify(names)
    else:
        data = {
            'data': data,
            'bool': False,
            'content': data_type
        }
        #return jsonify(data_type)
    #если хочется посмотреть в форме, я её сделала так как 
    #не так поняла задание как надо было
    return render_template('index.html', **data, amount=amount)


if __name__ == '__main__':
    app.run(debug=True)
