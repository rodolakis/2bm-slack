import os
import time
import pathlib
from dotenv import load_dotenv
from datetime import datetime
from slack_bolt import App 
from slack_bolt.adapter.socket_mode import SocketModeHandler 
import pv
import log

# Set bot tokens as environment values
env_path = os.path.join(str(pathlib.Path.home()), '.slackenv')
load_dotenv(dotenv_path=env_path)

bot_token = os.environ.get("BOT_TOKEN")
app_token = os.environ.get("APP_TOKEN") 

app = App(token = bot_token)

@app.event("message") 
def reply(payload, say, client): 
    try: 
        text = payload["text"].lower()
    except: 
        return 
    user = client.users_info(user=payload["user"])["user"]["real_name"] 
    chan = client.conversations_info(channel=payload["channel"])["channel"]["name"]

    pvs = {}
    if chan == "2-bm": 
        if 'status' in text: 
            _, slack_message = pv.check_pvs_connected(pv_user)
            print (slack_message)
            say("status: ....")
        elif 'scan' in text: 
            say("scan: ....")
        elif 'user' in text: 
            say("user: ...") 
        elif 'help' in text: 
            say("help: ...") 
    elif chan == "automated": 
        f_dict = {'ring': pv.epics_ring, 'eps': pv.epics_eps, 'energy': pv.epics_energy, 
                   'optics': pv.epics_optics, 'sample': pv.epics_sample, 'user': pv.epics_user, 
                   'data': pv.epics_data, 'scan': pv.epics_scan, 'file': pv.epics_file, 
                   'detector': pv.epics_detector}
        if text in f_dict:
            pvs = f_dict[text]('2bm:', '2bmb:TomoScan:', '2bmbPG1:', '2bmbPG1:HDF1:')
            time.sleep(1)
            _, slack_messages = pv.check_pvs_connected(pvs)
            for message in slack_messages:
                say(message)
        elif text == 'help':
            for text in f_dict:
                say(text)
    else:
        if text_match(text, "hello"):
            say("Greetings *{0}*!".format(user)) 


if __name__ == "__main__": 
    # set logs directory
    home = os.path.expanduser("~")
    logs_home = home + '/logs/'
    # make sure logs directory exists
    if not os.path.exists(logs_home):
        os.makedirs(logs_home)
    # setup logger
    lfname = logs_home + 'slack_' + datetime.strftime(datetime.now(), "%Y-%m-%d_%H:%M:%S") + '.log'
    log.setup_custom_logger(lfname)

    SocketModeHandler(app, app_token).start() 
