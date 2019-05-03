import platform
import logging
logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)
for name in (['werkzeug','engineio','socketio','transitions']):
    logging.getLogger(name).setLevel('WARNING')

import common
import StateMachines

common.CDS = common.CommonDataStructure()
common.CDS.write('platform', platform.system())
common.CDS.write('testmode', {'Linux':False, 'Windows':True}[common.CDS.read('platform')])
common.Paths = common.Paths(common.CDS.read('platform'))

common.OpMode = StateMachines.OpModeMachine()
common.Active = StateMachines.ActiveMachine()

import HardwareController
import InterfaceManager
import MotionController
import NetController
import POST
import Setup

common.HardwareController = HardwareController.main()
common.InterfaceManager = InterfaceManager.main()
common.MotionController = MotionController.main()
common.NetController = NetController.main()
common.POST = POST.main()
common.Setup = Setup.main()

# Start transitioning
common.OpMode.toSetup()
common.CDS.start_logging(common.Paths['DATABASE'])
common.OpMode.toTest()
common.OpMode.toNormal()

while True:
    pass