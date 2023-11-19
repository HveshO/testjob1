import requests

base_url = 'http://127.0.0.1:5000'
# 1. Некорректный ввод данных
# 2. проверка всех типов полей
# 3. проверка всех типов полей с совпадением в базе
# в url %2B это +, пробел это %20
input_data = [
    '', 'uert', 'erlt&ejrtjt', 'woeiurrurr,elrijt', 'eirttu;weljrrjr', 'eroiterut&dfkjgjgjg', 'f_name1=weiruruur%lkretutu%hfhfh&', 'f_name1=weiruruur  lkretutu%hfhfh', 'b2=23.08.2023&b2=twoet', '&=&='
    'wielrttut=%2B70394595595&jrhjrht=oweiutut@mail.com&sldkfjsdkgj=2000-05-29&ksjdhghg=0000-00-00&kwehrewh=83.91.1000&lretjerjt=%2B799999999999999999',
    'field_a=phone&field_b=%2B7%20039%20459%2055%2095&field_c=irrrr.hhhh.perot@lishf.ru&field_d=21.09.2000', 'phone=%2B79999999999&lead_email=123gfjdf@mail.com'
]
for input in input_data:
    response_post = requests.post(f'{base_url}/get_form?{input}')
    print('POST Response:', response_post.text, response_post.status_code)
