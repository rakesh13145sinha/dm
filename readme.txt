pip install python-dotenv
pip install razorpay
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 >project.json
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 > project.json

[-h] [--format FORMAT] [--indent INDENT]
                          [--database DATABASE] [-e EXCLUDE]
                          [--natural-foreign] [--natural-primary] [-a]
                          [--pks PRIMARY_KEYS] [-o OUTPUT] [--version]
                          [-v {0,1,2,3}] [--settings SETTINGS]
                          [--pythonpath PYTHONPATH] [--traceback] [--no-color]
                          [--force-color] [--skip-checks]
                          [app_label[.ModelName] ...]

app lable
++============================ 
python manage.py dumpdata myapp1 myapp2.my_model
python manage.py dumpdata [app_label[.Model Name] [app_label [.ModelName]]]
python manage.py dumpdata app_label.ModelName > project.json
python manage.py dumpdata myapp2.my_model myapp2.my_model
python manage.py dumpdata myapp2 myapp2.my_model
python manage.py dumpdata -e contenttypes -e admin -e sessions -e auth.Permission  --indent 4 >backup/all.json
ssh -i "dw.pem" ubuntu@ec2-52-72-255-130.compute-1.amazonaws.com


