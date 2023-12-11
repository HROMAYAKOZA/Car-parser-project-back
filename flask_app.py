from services import app, scheduler, db
from services.href import cities
from services.advertisement import updatingADS, insert_ad_to_Advertisement

if __name__ == "__main__":
    scheduler.add_job(id='Task of updating the database', func=updatingADS,
                      trigger="interval", seconds=3600)
    scheduler.start()

    app.run(debug=True, use_reloader=False)
