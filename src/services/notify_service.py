import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config.config import DATA_PATHS, Web, THRESHOLDS, COINS
from utils.logger import get_logger

logger = get_logger('service')
class NotifyService:
    def __init__(self):
        self.config_file = os.path.join(DATA_PATHS['notify'],"alert_config.json")
        self.load_config()
    
    def load_config(self):
        """Load alert configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = self.get_default_config()
                self.save_config()
            logger.info(f"Load json successfully")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = self.get_default_config()
        
    def get_default_config(self):
        """Get default alert configuration"""

        return {
            'email': {
            'enabled': bool(Web.EMAIL_USER and Web.EMAIL_PASSWORD and Web.NOTIFICATION_EMAIL),
            'smtp_server': Web.SMTP_SERVER,
            'smtp_port': int(Web.SMTP_PORT),
            'username': Web.EMAIL_USER,
            'password': Web.EMAIL_PASSWORD,
            'to_email': Web.NOTIFICATION_EMAIL
            },
           'thresholds': {
            'accuracy_drop': float(THRESHOLDS.get('r2', 0.05)),
            'mse_increase': float(THRESHOLDS.get('mse', 0.20)),
        },
        'coins': COINS,
        'check_interval': 3600
        }
    
    
    def save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Saved loggers sucessfully")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def configure_alerts(self, new_config):
        """Update alert configuration"""
        try:
            self.config.update(new_config)
            self.save_config()
            logger.info(f"Configuration updated with: {new_config}")
            return {'status': 'success', 'message': 'configuration updated'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def check_thresholds(self, coin, current_metrics: dict, previous_metrics: dict):
        """Check if any thresholds are breached"""
        alerts = []
        thresholds = self.config['thresholds']

        # Check accuracy drop
        if 'accuracy' in current_metrics:
            if previous_metrics and 'accuracy' in previous_metrics:
                accuracy_drop = previous_metrics['accuracy'] - current_metrics['accuracy']
                
                if accuracy_drop > thresholds['accuracy_drop']:
                    alerts.append({
                        'type': 'accuracy_drop',
                        'message': f"Model accuracy dropped to {current_metrics['accuracy']:.2%} (Drop: {accuracy_drop:.2%})",
                        'severity': 'high',
                        'timestamp': current_metrics['timestamp'],
                        'coin': coin,
                        'status': 'activate'
                                       
                    })
        # Check MSE increase 
        if 'mse' in current_metrics and previous_metrics and 'mse' in previous_metrics:
            mse_increase = (current_metrics['mse'] - previous_metrics['mse']) / previous_metrics['mse']
            if mse_increase > thresholds['mse_increase']:
                    alerts.append({
                        'type': 'mse_increase',
                        'message': f"MSE increased by {mse_increase:.1%}",
                        'severity': 'medium',
                        'timestamp': current_metrics['timestamp'],
                        'coin': coin,
                        'status': 'activate'
                    })  
        return alerts    
        
    def send_email_alerts(self, subject: str, message: str, coin: str):
        """Send email alerts if email notifications are enabled"""
        try:
            if not self.config['email']['enabled']:
                logger.warning(f"Email notifications disabled for {coin}")
                return {'status': 'disabled'}
            if not all([
                self.config['email']['username'], 
                self.config['email']['password'], 
                self.config['email']['to_email']
                ]):
                logger.warning("Email configuration incomplete")
                return {'status': 'error', 'message': 'Email configuration incomplete'}
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['username']
            msg['To'] = self.config['email']['to_email']
            msg['Subject'] = f"[Crypto Prediction Alert] {subject} - {coin.upper()}"

            # Add body
            body = f"""\
            Alert for {coin.upper()}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            {message}

            Please check your dashboard for more details.
            """
            msg.attach(MIMEText(body, 'plain'))

            # Send email
            server = smtplib.SMTP(self.config['email']['smtp_server'],
                                  self.config['email']['smtp_port'])
            
            server.starttls()
            server.login(self.config['email']['username'],
                         self.config['email']['password'])
            text = msg.as_string()
            server.sendmail(self.config['email']['username'],
                            self.config['email']['to_email'], text)
            
            server.quit()
            logger.info(f"Email alert send for {coin}: {subject}")

            return {'status': 'sent'}
        
        except Exception as e:
            logger.error(f"Email error: {e}")
            return {'status': 'error', 'message': str(e)}
   
    def get_alert_history(self):
        """Retrieve alert history (stub for future database integration)"""
        history_file = os.path.join(DATA_PATHS['notify'],"alert_history.json")
        try:
            if not os.path.exists(history_file):
                os.makedirs(os.path.dirname(history_file), exist_ok=True)
                with open(history_file, 'w') as f:
                    json.dump([], f)
            with open(history_file, 'r') as f:
                return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading alert history: {str(e)}")
            return []