#!/bin/sh

# Author: Bart van Strien
#         Mathijs van de Nes
# Date:   2014-01-07
# 
# Een script om het kopieren van een hardeschijf te monitoren.
# Opmerkingen: Mountpoint was /sata, drive was /dev/sda, en totale grootte was 105 GB
#

while true; do df -h /sata | grep /dev/sda | sed 's/\s\s*/ /g' | cut -d' ' -f 3 | sed 's/G//' | awk '{print $0/1.05}' | cut -d. -f1; sleep 2; done | dialog --gauge "Kopieren" 7 50
