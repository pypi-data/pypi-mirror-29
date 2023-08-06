# BetterConfig client for Python
BetterConfig is a cloud based configuration as a service. It integrates with your apps, backends, websites,
and other programs, so you can configure them through the [BetterConfig website](https://betterconfig.com) even after they are deployed.

[![Build Status](https://travis-ci.org/BetterConfig/BetterConfigClient-python.svg?branch=master)](https://travis-ci.org/BetterConfig/BetterConfigClient-python) [![codecov](https://codecov.io/gh/BetterConfig/BetterConfigClient-python/branch/master/graph/badge.svg)](https://codecov.io/gh/BetterConfig/BetterConfigClient-python) [![PyPI version](https://badge.fury.io/py/betterconfigclient-python.svg)](https://badge.fury.io/py/betterconfigclient-python)

## Getting started

**1. Install the BetterConfigClient-Python package with `pip`**

```bash
pip install betterconfigclient-python
```

**2. Import `betterconfigclient` to your application**

```python
import betterconfigclient
```

**3. Get your Project Secret from [BetterConfig.com](https://betterconfig.com) portal**

![YourConnectionUrl](https://raw.githubusercontent.com/BetterConfig/BetterConfigClient-dotnet/master/media/readme01.png  "YourProjectSecret")

**4. Configure the client**

```python
betterconfigclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>')
client = betterconfigclient.get()
```

**5. Get your config value**
```python
isMyAwesomeFeatureEnabled = client.get_value('key-of-my-awesome-feature', False)
if isMyAwesomeFeatureEnabled:
    //show your awesome feature to the world!
```

**6. It is recommended to close the BetterConfigClient during the shutdown of your application**
```python
betterconfigclient.close()
```

## Configuration

### Default cache
By default the BetterConfig client uses a built in in-memory cache implementation, which can be customized with the following configurations:

##### Time to leave (TTL)
You can define the TTL of the cache in seconds (min: 1 sec, default: 60 sec). This value will be used to determine how much time must pass before initiating a new configuration fetch request through the `ConfigFetcher`.
```python
betterconfigclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>', time_to_live_seconds=120)
```

### Custom cache
You also have the option to use your custom cache implementation in the client. All you have to do is to create an implamentation from the `ConfigStore` interface, and pass it to the client initialization:
```python
class YourCustomConfigStore(ConfigStore):
    def __init__(self, config_fetcher):
        self._config_fetcher = config_fetcher

    def get(self):
        # If the cache is invalid, you can fetch it through the _config_fetcher
        # try:
        #     json = self._config_fetcher.get_configuration_json()
        #     Store the configuration to your cache
        # except HTTPError as e:
        #     log.error('Received unexpected response from ConfigFetcher ' + str(e.response))
        # except:
        #     log.exception(sys.exc_info()[0])
        pass

    def invalidate_cache(self):
        pass

betterconfigclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>', config_store_class=YourCustomConfigStore)
```

### Logging
The BetterConfig client uses the default Python `logging` package for logging.