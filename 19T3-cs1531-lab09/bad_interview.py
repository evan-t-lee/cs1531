def bad_interview():
    '''
    A generator that yields all numbers from 1 onward, but with some exceptions:
    * For numbers divisible by 3 it instead yields "Fizz"
    * For numbers divisible by 5 it instead yields "Buzz"
    * For numbers divisible by both 3 and 5 it instead yields "FizzBuzz"
    '''
    num = 1
    while True:
        yieldVal = ''
        if not num % 3:
            yieldVal += 'Fizz'
        if not num % 5:
            yieldVal += 'Buzz'
        yield yieldVal if yieldVal else num
        num += 1
