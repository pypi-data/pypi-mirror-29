# Copyright 2015-2017 F-Secure

# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License.  You may
# obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.

"""Module for triggering time based events."""

from threading import Timer

from see import Hook


class TimersHook(Hook):
    """
    Timers hook.

    Allows to trigger events at given times.

    configuration::

        {
          "timers": {"event_to_trigger_after_40_seconds": 40}
        }

    Timers are started during Hook's initialization.

    """
    def __init__(self, parameters):
        super().__init__(parameters)

        self.timers = tuple(
            Timer(t, self.context.trigger, args=(e, ))
            for e, t in self.configuration.get('timers', {}).items())

        for timer in self.timers:
            timer.daemon = True
            timer.start()

    def cleanup(self):
        for timer in self.timers:
            timer.cancel()
