# -*- coding: utf-8 -*-

import time

from django.core.management.base import BaseCommand

from arm.models.device import ArmDevice, DeviceNotFound, USBError
from arm.constants import SLEEP_TIME


class Command(BaseCommand):
    """
    (暂弃)
    守护进程循环fetch设备，维护fetch状态
    """
    help = "Fetch the Arm from USB Device, endless loop until fetch success."

    def handle(self, *args, **options):
        last_exception = None
        while True:
            try:
                ArmDevice.fetch()
                print 'Fetch Arm Success!!'
                print 'sleep..'
            except (USBError, DeviceNotFound) as e:
                if e.__class__ != last_exception.__class__:
                    print 'ERROR, {}'.format(e)
                    last_exception = e
                    print 'loop fetch every {}s...'.format(SLEEP_TIME)
            time.sleep(SLEEP_TIME)
