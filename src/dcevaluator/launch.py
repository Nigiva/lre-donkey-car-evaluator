import begin
import sys
from loguru import logger

from dcevaluator.communication.dc_client import DonkeyCarClient
from dcevaluator.hardware.joystick import JoystickController
from dcevaluator.event.event_handler import EventHandler
from dcevaluator.controller.auto_controller import AutoController
from dcevaluator.evaluator.evaluator import Evaluator
from dcevaluator.controller.brain import Brain
from dcevaluator.utils.utils import build_log_tag

logger.remove()
logger.add(sys.stdout, level="INFO")

@begin.start
def run(evaluation_name = "No Name", host = "127.0.0.1", port = "9091", evaluation_scene = "roboracingleague_1"):
    logger.info(build_log_tag("Donkey Car Evaluator", "BEGIN"))
    logger.info(build_log_tag(evaluation_name=evaluation_name))
    logger.info(build_log_tag(host=host))
    logger.info(build_log_tag(port=port))
    logger.info(build_log_tag(evaluation_scene=evaluation_scene))

    event_handler = EventHandler()

    client = DonkeyCarClient(event_handler, host, int(port))
    client.connect()
    client.send_load_scene_request(evaluation_scene)

    #hardware = JoystickController()
    #controller = ManualController(client, hardware, event_handler)
    model_path = "/home/nigiva/git/lopilo-trainer/data/model/extern/DCDeepModelV4.0-reda-renault-speed_accel_gyro-batch128-1620155768.1678748"
    brain = Brain(model_path)
    controller = AutoController(client, brain, event_handler)

    evaluator = Evaluator(event_handler, controller)


