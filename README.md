# A bot to collect the form information and push it

---

## Tree:

```
└── src
    ├── dbServer.py
        > push and check out data
    ├── example.config.yml
        > config file
    ├── parseCfg.py
        > parse the configuration file
    └── tgBot.py
        > Collect and push messages
```

## Use

Before you run this bot, you need to configure the postgresql and redis, then copy `config.example.yml` as `config.yml` to fill in your configuration.

```shell
pip install -r requirements.txt
cd src
python3 tgBot.py
```
