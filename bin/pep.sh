#!/usr/bin/env bash


run_pep_once() {
    # Execute the backend system process chain
    # 1. pull requests
    # 2. run PEP
    # 3. run PMP to update policy direcory in git /unsigned
    # 4. push results

    cd /repo
    git fetch
    git merge -m 'merge uploads' origin/master >> /var/log/polman/pep.lastlog 2>> /var/log/polman/pep.lasterr

    pep.sh >> /var/log/polman/pep.lastlog 2>> /var/log/polman/pep.lasterr
    dump_poldir.sh >> /var/log/polman/pep.lastlog 2>> /var/log/polman/pep.lasterr

    git add unsigned >> /var/log/polman/pep.lastlog 2>> /var/log/polman/pep.lasterr
    git commit -m 'updated/generated by PEP' >> /var/log/polman/pep.lastlog 2>> /var/log/polman/pep.lasterr
    git push >> /var/log/polman/pep.lastlog 2>> /var/log/polman/pep.lasterr
}


run_pep_forever() {
    while true
    do
        printf "$(date --iso-8601=seconds) starting pep\n" > /var/log/polman/pep.lastlog
        printf "$(date --iso-8601=seconds) starting pep\n" > /var/log/polman/pep.lasterr
        # pep.lastlog can be used as container liveness check
        run_pep_once
        egrep -v '(PolicyManager Version|Already up-to-date|On branch master|nothing to commit,)' /var/log/polman/pep.lastlog
        egrep -v 'Everything up-to-date' /var/log/polman/pep.lasterr 1>&2
        sleep $PEP_FREQUENCY_SECONDS
    done
}


run_pep_forever