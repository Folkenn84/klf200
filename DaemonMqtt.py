import daemon

from Mqtt import main

with daemon.DaemonContext():
    main()