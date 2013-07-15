#!/usr/bin/env python3.3

import os
import rea


def latency_conpensation(users, target=0, default_latency=0):

    with rea.newTask("Adjust Compensation") as project:
        for track in project.tracks:
            username = track.name.split("@")[0]
            latency = users.get(username, default_latency)

            if not latency:
                continue

            for item in track.items:
                pos = item.position + latency
                if pos >= 0:
                    item.position = pos
            else:
                rea.show_message("{} moved {:0.4}ms\n".format(username,latency))


if __name__ == "__main__":

    table_file = os.path.join(rea.getScriptPath(), "LatencyTable.txt")
    users = rea.loadTable(table_file)

    latency_conpensation(users, default_latency=0)
