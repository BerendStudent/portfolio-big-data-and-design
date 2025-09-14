
oreo = {
    'cal': 210,
    'fat': 10.5,
    'carbohydrates': 27,
    'protein': 2
}

oreo_nutrition = {}
overeating = False

for field in oreo:
    oreo_nutrition[field] = oreo[field] / 2

number_ate = int(input('How many cookies did you eat? '))

for field in oreo_nutrition:
    number = oreo_nutrition[field] * number_ate
    print(field, "consumed: ", number)
    if field == 'cal' and number > 750:
        overeating = True

if overeating:
    print('Stop eating those damned delicious cookies!')