#!/bin/bash

python /root/opt/BinanceDB/BinanceTableModel.py
python /root/opt/BinanceDB/GetInitialData.py

/bin/sh /root/opt/setup-cron.sh