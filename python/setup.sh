#!/bin/bash

python /root/opt/BinanceDB/BinanceTableModel.py
python /root/opt/BinanceDB/GetSymbolData.py
python /root/opt/BinanceDB/GetSymbolDataSpot.py
python /root/opt/BinanceDB/GetInitialData.py
python /root/opt/TechnicalDB/TechnicalTableModel.py

python /root/opt/TechnicalDB/HighSchool.py

/bin/sh /root/opt/setup-cron.sh