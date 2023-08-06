# BetterConfig client for Python
BetterConfig is a cloud based configuration as a service. It integrates with your apps, backends, websites, and other programs, so you can configure them through this website even after they are deployed.
https://betterconfig.com  

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

**3. Get your Project Secret from the [BetterConfig.com](https://betterconfig.com) portal**

![YourConnectionUrl](https://raw.githubusercontent.com/BetterConfig/BetterConfigClient-dotnet/master/media/readme02.png  "YourProjectSecret")

**4. Initialize and get the client**

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

**6. On application exit:**
```python
betterconfigclient.stop()
```

## Configuration
Client supports three different caching policies to acquire the configuration from BetterConfig. When the client fetches the latest configuration, puts it into the internal cache and serves any configuration acquisition from cache. With these caching policies you can manage your configurations' lifetimes easily.

### Auto polling (default)
Client downloads the latest configuration and puts into a cache repeatedly. Use ```poll_interval_seconds``` parameter to manage polling interval.
Use ```on_configuration_changed_callback``` parameter to get notification about configuration changes. 

### Lazy loading
Client downloads the latest configuration only when it is not present or expired in the cache. 
Use ```cache_time_to_live_seconds``` parameter to manage configuration lifetime.

### Manual polling
With this mode you always have to call ```force_refresh()``` method to fetch the latest configuration into the cache. When the cache is empty (for example after client initialization) and you try to acquire any value you'll get the default value!

---

Initializing the client and the configuration parameters are different for each cache policy:

### Auto polling  
```betterconfigclient.initialize(...)```

| ParameterName        | Description           | Default  |
| --- | --- | --- |
| ```project_secret```      | Project Secret to access your configuration  | REQUIRED |
| ```poll_interval_seconds ```      | Polling interval|   60 | 
| ```max_init_wait_time_seconds```      | Maximum waiting time between the client initialization and the first config acquisition in secconds.|   5 |
| ```on_configuration_changed_callback```      | Callback to get notification about configuration changes. |   None |
| ```config_cache_class```      | Custom cache implementation class. |   None |

#### Example - increase ```poll_interval_seconds``` to 600 seconds:

```python
betterconfigclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>', poll_interval_seconds=600)
```

#### Example - get notification about configuration changes via ```on_configuration_changed_callback```:  

```python
def configuration_changed_callback(self):
    # Configuration changed.
    pass
    
betterconfigclient.initialize('<PLACE-YOUR-PROJECT-SECRET-HERE>', on_configuration_changed_callback=configuration_changed_callback)
```

### Lazy loading
```betterconfigclient.initialize_lazy_loading(...)```

| ParameterName        | Description           | Default  |
| --- | --- | --- | 
| ```project_secret```      | Project Secret to access your configuration  | REQUIRED |
| ```cache_time_to_live_seconds```      | Use this value to manage the cache's TTL. |   60 |
| ```config_cache_class```      | Custom cache implementation class. |   None |

#### Example - increase ```cache_time_to_live_seconds``` to 600 seconds:

```python
betterconfigclient.initialize_lazy_loading('<PLACE-YOUR-PROJECT-SECRET-HERE>', cache_time_to_live_seconds=600)
```

#### Example - use a custom ```config_cache_class```:

```python
from betterconfigclient.interfaces import ConfigCache


class InMemoryConfigCache(ConfigCache):

    def __init__(self):
        self._value = None

    def get(self):
        return self._value

    def set(self, value):
        self._value = value

betterconfigclient.initialize_lazy_loading('<PLACE-YOUR-PROJECT-SECRET-HERE>', config_cache_class=InMemoryConfigCache)
```

### Manual polling
```betterconfigclient.initialize_manual_polling(...)```

| ParameterName        | Description           | Default  |
| --- | --- | --- | 
| ```project_secret```      | Project Secret to access your configuration  | REQUIRED |
| ```config_cache_class```      | Custom cache implementation class. |   None |

#### Example - call ```force_refresh()``` to fetch the latest configuration:

```python
betterconfigclient.initialize_manual_polling('<PLACE-YOUR-PROJECT-SECRET-HERE>')
betterconfigclient.get().get_value('test_key', 'default_value') # This will return 'default_value' 
betterconfigclient.get().force_refresh()
betterconfigclient.get().get_value('test_key', 'default_value') # This will return the real value for key 'test_key'
```

## Members
### Methods
| Name        | Description           |
| :------- | :--- |
| ``` betterconfigclient.get().get_configuration_json() ``` | Returns configuration as a json dictionary |
| ``` betterconfigclient.get().get_value(key, defaultValue) ``` | Returns the value of the key |
| ``` betterconfigclient.get().force_refresh() ``` | Fetches the latest configuration from the server. You can use this method with WebHooks to ensure up to date configuration values in your application. |

## Logging
The BetterConfig client uses the default Python `logging` package for logging.

## Sample projects
* [Console sample](https://github.com/BetterConfig/BetterConfigClient-python/tree/master/samples/consolesample)
* [Django web app sample](https://github.com/BetterConfig/BetterConfigClient-python/tree/master/samples/webappsample)