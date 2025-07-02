"""Tracks model performance metrics"""
import pandas as pd
import os
from datetime import datetime
from utils.logger import get_logger
from utils.helper import validate_dataframe, ensure_directory
from config.config import DATA_PATHS
from services.notify_service import NotifyService

logger = get_logger('monitor')
notify_service = NotifyService()

def monitor_metrics(coin: str) ->  dict:
    """Monitor metrics for a given coin and trigger alerts if thresholds are breached"""
    try:
        metrics_file = os.path.join(DATA_PATHS['perform_metrics'],f'{coin}_performance_metrics.csv')
        
        ensure_directory(DATA_PATHS['perform_metrics'])
        df = pd.read_csv(metrics_file)
        if df.empty:
            logger.error(f"Loaded data is empty from path {metrics_file}")

        # Get the latest metrics
        current_metrics = df.iloc[-1].to_dict()
        current_metrics['coin'] = coin
        current_metrics['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Load previous metrics if available
        previous_metrics = df.iloc[-2].to_dict() if len(df) > 1 else {}

        alerts = notify_service.check_thresholds(coin, current_metrics, previous_metrics)
        logger.info(f"{len(alerts)} alerts triggered for {coin}")

        for alert in alerts:
            notify_service.send_email_alerts(
                subject=alert['type'].replace('_', ' ').title(),
                message=alert['message'],
                coin=coin
            )
        logger.info("Send alert successfully")

        return {"status": "success", "alerts": alerts}
    except Exception as e:
        logger.error(f"Error monitoring metrics for {coin}: {str(e)}")
        return {"status": "error", "message": str(e)}
 


   

    


    # # Compare with thresholds
    # alerts = []
    # if mae > THRESHOLDS["mae"]:
    #     alerts.append(f"MAE too high: {mae:.3f} > {THRESHOLDS['mae']}")

    # if mse > THRESHOLDS["mse"]:
    #     alerts.append(f"Accuracy too low: {mse:.3f} < {THRESHOLDS['mse']}")
        
    # if r2 < THRESHOLDS["r2"]:
    #     alerts.append(f"r2 too low: {r2:.3f} < {THRESHOLDS['r2']}")

    # # Send alerts if needed
    # if alerts:
    #     message = "\n".join(alerts)
    #     send_alert(message)
    # else:
    #     print(f"Model performance is within acceptable limits")
    


