from python
run apt update -y
run apt install -y gcc git

run cd /opt && git clone https://github.com/raydoom/mmanager.git 
run pip3 install -r /opt/mmanager/requirements.txt -i http://mirrors.aliyun.com/pypi/simple  --trusted-host mirrors.aliyun.com

expose 8000

cmd python3 /opt/mmanager/manage.py runserver 0.0.0.0:8000

