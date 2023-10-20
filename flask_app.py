from services import app, scheduler, db
from services.advertisement import updatingADS

scheduler.add_job(id='Task of updating the database', func=updatingADS, trigger="interval", seconds=500)
scheduler.start()

app.run(debug=True, use_reloader=False)
