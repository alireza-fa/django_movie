from accounts.tasks import send_mail_task


def send_email(subject: str, body: str, receiver_list: list):
    return send_mail_task.delay(subject, body, receiver_list)
