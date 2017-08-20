# Monitor

## Cliente

- Instalarlo en la RaspberryPi
- Agregarlo al Crontab:

```
# crontab -e

*/2 * * * * python $HOME/dev/monitor/client/run.py
```

### Servidor

#### Status Server

- Instalarlo en el Server
- Para iniciar: `python server/server.py`

#### Monitor de Connectividad

- Instalarlo en el Server
- Agregarlo al Crontab:

```
# crontab -e

*/2 * * * * python $HOME/dev/monitor/server/monitor.py
```

