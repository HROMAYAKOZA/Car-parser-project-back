from services import app, scheduler
from services.advertisement import updatingADS
from waitress import serve

if __name__ == "__main__":
    scheduler.add_job(id='Task of updating the database', func=updatingADS,
                      trigger="interval", seconds=3600)
    scheduler.start()

    serve(app, host='0.0.0.0', port=5000)
