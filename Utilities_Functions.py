prize_dict = {
    'grand_prize'   : ('特別獎', '1,000萬'),
    'special_prize' : ('特獎', '200萬'),
    'top_prize'     : ('頭獎', '20萬'),
    'second_prize'  : ('二獎', '4萬'),
    'third_prize'   : ('三獎', '1萬'),
    'fourth_prize'  : ('四獎', '4000'),
    'fifth_prize'   : ('五獎', '1000'),
    'sixth_prize'   : ('六獎', '200'),
}

def parse_results(results):
    if type(results) == dict:
        months = list(results.keys())[0]
        prize = prize_dict[list(results.values())[0]]
        return '恭喜中了{}月的{}\n獎金 {} 元'.format(months, prize[0], prize[1])
    elif 'no hit' in results:
        return '沒中'
    else:
        return '號碼需為3位以上的數字'

def numerical(character):
    try:
        int(character)
        return True
    except ValueError:
        return False
        
def filter_inputs(text):
    return ''.join([t for t in text if numerical(t)])
