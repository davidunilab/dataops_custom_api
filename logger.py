import logging
log = logging.basicConfig(
    filename="app.log", 
    level=logging.INFO, 
    filemode="w",
    format='[%(asctime)s] %(levelname)s: %(message)s'
    )