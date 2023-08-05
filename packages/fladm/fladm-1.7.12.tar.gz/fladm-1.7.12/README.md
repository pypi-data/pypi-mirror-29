# Flamingo cli tool

파이썬으로 개발된 플라밍고 관리 툴입니다.

개발서버, 데모서버들을 관리하는데 도움을 줍니다.

1. 로그 보기 (showlog)
2. 서버 기동 (service [start|stop|restart])
3. 상태 보기 (status | status-all)
4. HDFS 업로드 (upload)

## 설치방법
### pip
```bash
$ sudo -H pip install --ignore-installed six
$ sudo -H pip install fladm --no-cache-dir
```

### source
```bash
$ git clone http://gitlab.exem-oss.org/flamingo/flamingo-adm-cli.git
$ cd flamingo-adm-cli
$ sudo -H python setup.py install
$ sudo -H pip install paramiko
```

## 실행방법
```bash
$ fladm showlog dev.was
$ fladm service demo.jupyter stop
$ fladm status-all

$ flcli login -user=exem -pw=1234 -domain=flamingo.exem-oss.org
$ flcli upload -source=README.md -dest=/usr/README.md
$ flcli upload -source=README.md -dest=/usr/README.md -own=hive -group=hive -permission=755
```

## 스크린샷
<img src="capture/showlog_exam_01.png" width="600" />
<img src="capture/service_exam_01.png" width="600" />
<img src="capture/status-all_exam_01.png" width="600" />

## 서버 추가방법
flamingo-cli-config.json 파일을 아래와 같이 수정합니다. 추가 또는 삭제
```json
{
    "showlog":{
        ...
        "dev.web":{
            "host":"fem.exem.oss",
            "path":"/opt/exem/flamingo/current/web/logs/catalina.out"
        },
        ...
    },
    "service":{
        ...
        "dev.web":{
            "host":"fem.exem.oss",
            "user":"flamingo",
            "path":"/opt/exem/flamingo/current/web/bin/",
            "start":"startup.sh",
            "stop":"shutdown.sh",
            "restart":"shutdown.sh;startup.sh"
        },
        ...
    }
}
```


## 배포 방법
```bash
$ sudo -H pip install twine
```

```bash
$ cd [sourceDir]
$ sudo -H python setup.py sdist
$ twine upload dist/*
```