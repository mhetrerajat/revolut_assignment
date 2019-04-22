from flask import jsonify


class ApiException(Exception):
    def __init__(self, message, status=400, *args, **kwargs):
        self.message = message
        self.status = status

    def get_response(self):
        return jsonify({
            'data': None,
            'message': self.message,
            'status': 'failed'
        }), self.status


class UserAlreadyExistsException(ApiException):
    def __init__(self, username, *args, **kwargs):
        message = "User {0} already exists. Please use different username.".format(
            username)
        super(UserAlreadyExistsException,
              self).__init__(message, *args, **kwargs)


class RequirementParameterMissing(ApiException):
    def __init__(self, params, *args, **kwargs):
        message = "One or more required parameters are missing. Required parameters are : {0}".format(
            ", ".join(params))
        super(RequirementParameterMissing, self).__init__(message, *args, **kwargs)
