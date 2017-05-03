import sys,os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../lib/python"))

from psychopy import visual, core, event, gui, data
from psychopy.iohub import launchHubServer
import random, time, datetime, os
from psychopy.tools.filetools import fromFile, toFile
from twisted.internet import reactor
from twisted.internet.task import LoopingCall, Cooperator
from actr6_jni import Dispatcher, JNI_Server, VisualChunk, Twisted_MPClock

actr_enabled = True

class Environment(object):

    if actr_enabled:
        d = Dispatcher()

    STATE_WAIT_CONNECT = -3
    STATE_WAIT_MODEL = -2
    STATE_INTRO = -1
    STATE_RESET = 0
    STATE_FIXATION = 1
    STATE_UPDATE = 2
    STATE_TASK = 3
    STATE_DONE = 4

    def __init__(self, actr=False):

        self.io = launchHubServer()
        self.keyboard = self.io.devices.keyboard
        self.win = visual.Window(size = (1280,1024), units='pix', color='white', colorSpace='rgb', allowGUI=False, screen=0, monitor='testMonitor')

        if random.randint(0,1) == 0:
            self.stimulus = "x"
        else:
            self.stimulus = "y"

        self.slide = visual.TextStim(self.win, text = self.stimulus, font = 'Courier Regular', alignHoriz = "center", height = 24, color = 'black', bold = True)

        xcoord = random.randint(-500, 500)
        ycoord = random.randint(-500, 500)
        self.slide.pos = (xcoord, ycoord)

        self.textstim = visual.TextStim(self.win, text = "Press any key to continue", font = 'Courier Regular', alignHoriz = "center", height = 24, color = 'black', bold = True, pos = (0,0))

        self.state = self.STATE_INTRO
        self.actr = actr
        self.actr_time_lock = False
        if self.actr:
            self.state = self.STATE_WAIT_CONNECT
            self.actr = JNI_Server(self, clock=Twisted_MPClock())
            self.actr.addDispatcher(self.d)
            reactor.listenTCP(5555, self.actr)

        self.lc1 = LoopingCall(self.update_env)
        self.lc1.start(1.0 / 30)

        self.coop = Cooperator()
        self.coop.coiterate(self.process_event())

    def reset(self):
        pass

    def draw_actr_wait_connect(self):
        self.textstim.text = "Waiting for ACT-R to connect..."
        self.textstim.draw()
        self.win.flip()

    def draw_actr_wait_model(self):
        self.textstim.text = "Waiting for ACT-R model"
        self.textstim.draw()
        self.win.flip()

    def draw_task(self):
        self.slide.draw()
        self.win.flip()
        if self.actr:
            stim = VisualChunk("stim1", "vis-stim", self.slide.pos[0] + 640, self.slide.pos[1] + 512, value=self.slide.text)
            self.actr.display_new([stim])
        key = event.getKeys()
        while len(key) == 0:
            key = event.getKeys()
            reactor.iterate()
        if key[0] == self.stimulus:
            self.slide.setText("Correct")
        else:
            self.slide.setText("Incorrect")
        self.slide.pos = (0,0)
        self.slide.draw()
        self.win.flip()
        if self.actr:
            feedback = VisualChunk("feedback1", "vis-stim", self.slide.pos[0] + 640, self.slide.pos[1] + 512)
            self.actr.display_new([feedback])
        core.wait(2)
        if self.actr:
            print 'stop reactor'
            reactor.stop()

    def draw_intro(self):
        self.textstim.text = "Press any key to continue"
        self.textstim.draw()
        self.win.flip()
        if self.actr:
            stim = VisualChunk(None, "vis-stim", int(self.textstim.pos[0] + 640), int(self.textstim.pos[1] + 512), value="z")
            self.actr.display_new([stim])

    def update_env(self):
        if self.state == self.STATE_WAIT_CONNECT:
            self.draw_actr_wait_connect()
        if self.state == self.STATE_WAIT_MODEL:
            self.draw_actr_wait_model()
        if self.state == self.STATE_INTRO:
            while len(event.getKeys()) == 0:
                reactor.iterate()
            self.state = self.STATE_TASK
        if self.state == self.STATE_RESET:
            self.reset()
            self.state = self.STATE_TASK
        if self.state == self.STATE_TASK:
            self.draw_task()


    def handle_key_press(self, code, key):
        event._onPygletKey(code, 0)

    def process_event(self):
        yield

    def setDefaultClock(self):
        self.lc1.stop()
        self.lc1.clock = reactor
        self.lc1.start(1.0 / 30)

    if actr_enabled:

        @d.listen('connectionMade')
        def ACTR6_JNI_Event(self, model, params):
            self.state = self.STATE_WAIT_MODEL
            self.actr.setup(self.win.size[0], self.win.size[1])

        @d.listen('connectionLost')
        def ACTR6_JNI_Event(self, model, params):
            self.setDefaultClock()
            self.state = self.STATE_WAIT_CONNECT

        @d.listen('reset')
        def ACTR6_JNI_Event(self, model, params):
            self.actr_time_lock = params['time-lock']
            self.setDefaultClock()
            self.state = self.STATE_WAIT_MODEL

        @d.listen('model-run')
        def ACTR6_JNI_Event(self, model, params):
            if not params['resume']:
                self.state = self.STATE_INTRO
                # X = VisualChunk(None, "letterobj", self.intro_xs.centerx, self.intro_xs.centery, color=":red")
                # self.actr.update_display([X], clear=True)
                self.draw_intro()
                self.actr_running = True
            if self.actr_time_lock:
                self.lc1.stop()
                self.lc1.clock = self.actr.clock
                self.lc1.start(1.0 / 30)

        @d.listen('model-stop')
        def ACTR6_JNI_Event(self, model, params):
            pass

        @d.listen('keydown')
        def ACTR6_JNI_Event(self, model, params):
            self.handle_key_press(params['keycode'], chr(params['keycode']))

        @d.listen('mousemotion')
        def ACTR6_JNI_Event(self, model, params):
            pass

        @d.listen('mousedown')
        def ACTR6_JNI_Event(self, model, params):
            pass

if __name__ == '__main__':
    env = Environment(actr=actr_enabled)
    print 'starting reactor'
    reactor.run()
