from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models import Enterprise
from exceptions.admin_required_decorator import NotAllowedError

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        if(not current_user_id):
            raise NotAllowedError()
        
        current_user = Enterpris.get_some_user_id(current_user_id)
        if(not current_user or not current_user.is_admin):
            raise NotAllowedError()
        
        return f(*args, **kwargs)
            
    return decorated_function