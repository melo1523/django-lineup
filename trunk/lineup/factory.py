import os
import hashlib
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from lineup.models import Queue, QueueParam
from lineup.conf import Status
    
class JobFactory(object):
    """docstring for JobFactory"""
    
    def __init__(self):
        super(JobFactory, self).__init__()

    @transaction.commit_manually    
    def create_job(self, job, user, context_object, params, project = None, status = Status.new):
        _debug("Job Factory called for %s" % job)
        try:
            
            q = Queue()
            q.job = job
            q.user = user
            q.context_object = context_object
            q.status = status
            q.project = project
            q.save()
        
            for param_name, param_value in params.items():
                p = QueueParam()
                p.param_name = param_name
                p.queue = q
                if len(param_value) > 255:
                    p.param_value_long = param_value
                else:
                    p.param_value = param_value
        
                p.save()
                    
            transaction.commit()
        
            _debug("Job id: %s produced, yay." % q.id)
            
        except Exception, e:
            _debug("Exceptions during job creation. Raising.")
            transaction.rollback()
            raise
