#!/bin/bash
sed -i -e '/<<<<<<</,/=======/d' imputation.ipynb
sed -i -e '/>>>>>>>/d' imputation.ipynb
sleep 0.5