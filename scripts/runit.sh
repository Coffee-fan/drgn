#!/bin/bash -e
sudo python -m drgn -c ./vmcore -s ./vmlinux-5.2.9-241_fbk16_4245_g53e65cc15fc6 examples/linux/slabinfo.py
