"""
Test autorestart of infinite uninteruptable docker container after docker
daemon restart.

#. Stop system docker daemon
#. Start test docker daemon with special work dir (graph) path.
#. Start infinite docker container.
#. Restart docker daemon.
#. Check if docker container is auto restarted after docker restart.
"""
# pylint: disable=E0611
from restart import restart_container_autorestart_base


class restart_container_autorestart_int(restart_container_autorestart_base):

    def postprocess(self):
        super(restart_container_autorestart_int, self).postprocess()

        i = self.conts.get_container_metadata(self.sub_stuff["cont1_name"])
        self.failif(i is None,
                    "Container was probably not created.")

        daemon_stdout = ""
        daemon_stderr = ""
        if "docker_daemon" in self.sub_stuff:
            daemon_stdout = self.sub_stuff["docker_daemon"].get_stdout()
            daemon_stderr = self.sub_stuff["docker_daemon"].get_stderr()

        if not i[0]["State"]["Running"]:
            self.logdebug("\nDAEMON-STDOUT:\n"
                          "%s\nDAEMON-STDERR:\n%s" % (daemon_stdout,
                                                      daemon_stderr))

        self.failif(not i[0]["State"]["Running"],
                    "Container was not autorestarted after docker "
                    "daemon restart. Closer detail in debug.")
