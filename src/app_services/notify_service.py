import smtplib
from email.mime.text import MIMEText
from utils.logger import get_logger
from config.config import EMAIL_CONFIG

logger = get_logger('notification_service')

def send_notification(subject: str, body: str):
    """Send email notification"""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_CONFIG['user']
        msg['To'] = EMAIL_CONFIG['user']
        with smtplib.SMTP(EMAIL_CONFIG['host'], EMAIL_CONFIG['port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['user'], EMAIL_CONFIG['password'])
            server.sendmail(EMAIL_CONFIG['user'], EMAIL_CONFIG['password'])
        
        logger.info(f"Sent notification: {subject}")
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        raise 