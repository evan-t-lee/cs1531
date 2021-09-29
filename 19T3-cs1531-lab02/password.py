import re
def check_password(p):
 '''
 Takes in a password, and returns a string based on the strength of that password.

 The returned value should be:
 * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
 * "Moderate password", if at least 8 characters, contains at least one number.
 * "Poor password", for anything else
 * "Horrible password", if the user enters "password", "iloveyou", or "123456"
 '''
 r=lambda e:bool(re.search(e,p));s='password';i=p not in[s,'123456','iloveyou'];i+=r('\d')*len(p)>7
 if i>1:i+=r('[a-z]')*r('[A-Z]')*len(p)>11
 return['Horrible','Poor','Moderate','Strong'][i]+' '+s

if __name__ == '__main__':
	print(check_password('ihearttrimesters'))


def test_strong_password():
    assert check_password('Abcdefgh1234') == 'Strong password'
    assert check_password('passworD123456') == 'Strong password'

def test_moderate_password():
    assert check_password('Asdfghjk1') == 'Moderate password'
    assert check_password('asdfghjk1') == 'Moderate password'
    assert check_password('123456789123') == 'Moderate password'
    
def test_poor_password():
    assert check_password('asdfg1') == 'Poor password'
    assert check_password('ihearttrimesters') == 'Poor password'
    assert check_password('pAssword') == 'Poor password'
    assert check_password('654321') == 'Poor password'

def test_horrible_password():
    assert check_password('password') == 'Horrible password'
    assert check_password('iloveyou') == 'Horrible password'
    assert check_password('123456') == 'Horrible password'