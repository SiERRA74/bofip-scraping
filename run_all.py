from scraping import run_actu_links_scraping 
from info_harvestV2 import run_info_harvest

def bundle():
    run_actu_links_scraping()
    run_info_harvest()

