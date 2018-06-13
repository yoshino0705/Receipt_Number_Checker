import requests
from bs4 import BeautifulSoup

class Receipt_Numbers(object):
    def __init__(self):
        self._response = requests.request("GET","http://invoice.etax.nat.gov.tw/")
        self.soup = BeautifulSoup(str(self._response.content), 'html.parser')
        self._prize_numbers = self._get_prize_numbers()
    
    @staticmethod
    def _extract_lottery_number(tag):
        lottery_numbers = [t.contents[0].split('\\xe3\\x80\\x81') for t in tag]
        prize_names = ['grand_prize', 'special_prize', 'top_prize', 'sixth_prize'][:len(lottery_numbers)]
        return {k:v for k,v in zip(prize_names, lottery_numbers)}
    
    @staticmethod
    def _get_months(area_tags):
        h2 = area_tags[0].find_all('h2')
        month_tag = h2[1] # the second <h2> in area_tags
        months = month_tag.contents[0].replace('\\xe6\\x9c\\x88','').split('\\xe5\\xb9\\xb4')
        return months[1]
    
    @staticmethod
    def _get_prize_name(ranking):
        names = ['top', 'second', 'third', 'fourth', 'fifth', 'sixth']
        if ranking <= len(names):
            return '%s_prize' % names[ranking - 1]
        else:
            return 'no hit'
    
    @staticmethod
    def _valid_numbers(num_to_check):
        return False if type(num_to_check) != str or len(num_to_check) != 8 else True
    
    @staticmethod
    def generate_last_n_digits(digits):
        return [digits[i:] for i in range(len(digits))]
    
    @staticmethod
    def _check_top_prize_number(a_top_prize_num, num_to_check):
        min_len = min(len(a_top_prize_num), len(num_to_check))
        matches = 0
        for digit1, digit2 in zip(a_top_prize_num[::-1], num_to_check[::-1]):
            # [::-1] reverses string
            if digit1 == digit2:
                matches += 1
        return (8 - matches) + 1 if matches >= 3 else -1

    def _get_prize_numbers(self):
        tags = self.soup.find_all('table')
        latest_tags = tags[0].find_all(attrs={'class':"t18Red"})
        previous_tags = tags[1].find_all(attrs={'class':"t18Red"})
        lastest = Receipt_Numbers._extract_lottery_number(latest_tags)
        previous = Receipt_Numbers._extract_lottery_number(previous_tags)
        
        area1 = self.soup.find_all(attrs={'id':'area1'})
        area2 = self.soup.find_all(attrs={'id':'area2'})
        latest_months = Receipt_Numbers._get_months(area1)
        previous_months = Receipt_Numbers._get_months(area2)
        
        return [ {latest_months:lastest} , {previous_months:previous} ]
    
    def get_prize_numbers(self):
        return self._prize_numbers
    
    def _check_from_one_set(self, prizes_numbers, number_to_check):
        if not Receipt_Numbers._valid_numbers(number_to_check):
            return 'Invalid numbers'
        last_three_digits = number_to_check[len(number_to_check)-3 : ]
        if last_three_digits in prizes_numbers['sixth_prize']:
            return 'sixth_prize'
        if number_to_check in prizes_numbers['grand_prize']:
            return 'grand_prize'
        if number_to_check in prizes_numbers['special_prize']:
            return 'special_prize'
        results = [ Receipt_Numbers._check_top_prize_number(top, number_to_check) for top in prizes_numbers['top_prize'] ]
        results = [r for r in results if r != -1]
        if results:
            return Receipt_Numbers._get_prize_name(min(results)) # the lower the number the better prize
    
        return 'no hit'
    
    def check(self, numbers_to_check):
        _results = []
        for prize_numbers in self._prize_numbers:
            months = list(prize_numbers.keys())[0]
            hit_numbers = list(prize_numbers.values())[0]
            _results.append(
                {months :
                    self._check_from_one_set(hit_numbers, numbers_to_check)
                }                
            )
        
        _ret = []
        for _r in _results:   
            try:
                _ret.append([(_k,_v) for _k,_v in _r.items() if _v != 'Invalid numbers'][0])
            except IndexError:
                pass

        if _ret:
            _hits = [_r for _r in _ret if _r[1] != 'no hit']
            return _hits[0] if _hits else 'no hit'
        else:
            return 'Invalid numbers or input'
            
 if __name__ == '__main__':
     rn = Receipt_Numbers()
     num = '12342591'
     result = rn.check(num)
     print(result)
