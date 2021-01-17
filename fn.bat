@echo off
set "var=%cd%"
cd C:\Users\%USERNAME%\Python\Projects\FastNav
fn.py %*
cd %var%