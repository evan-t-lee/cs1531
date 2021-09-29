from werkzeug.exceptions import HTTPException

class AccessError(HTTPException):
    '''
    error to handle unauthorised attempts to perform actions
    '''
    code = 400
    message = "User is not authorised to perform this action."

class ValueError(HTTPException):
    '''
    redefinition of ValueError to better suit project requirements
    '''
    code = 400
    message = "Value syntax doesnt meet the requirements."
