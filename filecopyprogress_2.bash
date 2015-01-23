#!/bin/bash

# Author: Mathijs van de Nes
# Date:   2015-01-23
# 
# Een script om het kopieren van een hardeschijf te monitoren.
# Versie 2
#

dfrom='/sata'; dto='/mnt'; while true; do echo $(( 100 * $(df | grep $dto | awk '{print $3}') / $(df | grep $dfrom | awk '{print $3}') )); sleep 2; done | dialog --gauge "$dfrom -> $dto" 7 50
