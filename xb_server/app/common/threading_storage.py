import contextvars

user_id_var = contextvars.ContextVar('user_id')
job_id_var = contextvars.ContextVar('job_id')