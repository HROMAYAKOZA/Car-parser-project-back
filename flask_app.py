from services import app, scheduler, db
from services.advertisement import updatingADS

import time

# Sleep for 30 seconds
time.sleep(30)

scheduler.add_job(id='Task of updating the database', func=updatingADS, trigger="interval", seconds=3600)
scheduler.start()

app.run(debug=True, use_reloader=False)
