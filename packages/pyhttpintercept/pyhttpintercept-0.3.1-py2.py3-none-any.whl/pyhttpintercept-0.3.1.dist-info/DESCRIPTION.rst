# PyHTTPIntercept

Provides a HTTP Server which can be used to intercept and modify API requests/responses for local clients.

This is useful for client testing where generating different response types from the API is not always ideal.

The HTTP server provides the following functionality:

* Hosting of sites
* Redirecting requests with the following methods:
  * HTTP 3xx statuses
  * transparently to the client
* Intercepting and modifying of requests.  Man-in-the-middle, useful for client testing against a production API.
* Proxying of requests

When a request comes in methods are checked & executed in the following order:

1. Redirect
2. Hosting
3. Intercept - Intercept will only be reached if request is not picked up by hosting.
4. Proxy - Proxy configuration will only be reached if request is not picked up by Hosting or Intercept.


---

## Hosting requests

Sites can be hosted as with any webserver.  The server supports static sites/resources only.

### Hosting configuration

An example configuration file:

```JSON
{
  "/": {
    "doc_root": "default_sites/",
    "active": true,
    "description": "Root Site"
  },
  "/example": {
    "doc_root": "default_sites/example/",
    "active": true,
    "description": "Example Site"
  }
}
```

A configured site configurations key will be set to the expected url path.

Site configuration parameters:

* Object key: String - Path where site will be hosted.
* `doc_root`: String - The full path to the configured site. A relative path can also be configured and is explained below.
* `active`: Boolean - True if the site is to be served.
* `description`: String - [optional] A description for your site.

#### Relative paths
TODO


---

## Redirecting requests

### Sending HTTP 3xx statuses

These are your standard redirects.

### Transparently to the client

These are useful for clients that do not support redirects.

An example use would be redirecting a client with hard coded endpoints to a lab environemnt for testing without having to generate & install specific builds for the lab.

### Redirect configuration

Parameters:

* Object key: String - Domain to redirect.
* `host`: String - [optional] The full domain to redirect to.
* `paths`: Object - [optional] An object containing the paths being redirected for this domain.
* `active`: Boolean - True to enable redirect.
* `description`: String - [optional] A description for your redirect.

Note: at least one of `host` or `paths` must be specified!

Path object:

* Object key: String - Path to redirect.
* `host`: String - [optional] The full domain to redirect to.
* `path`: String - [optional] The full path to redirect to. If omitted then the path will be set to domain root.
* `status`: Number - [optional] The HTTP 3xx status to send.  Specifying this parameter tells the server to use a HTTP 3xx redirect rather than redirecting transparently.
* `active`: Boolean - True to enable redirect.
* `description`: String - [optional] A description for your redirect.

Note: at least one of `path` or `host` (from either site/path config) must be specified!

If a host is specifed in the key it will only by honoured when intercepting or proxying, for anything else the keys will be ignored.

Redirecting paths within the same site:

```JSON
{
  "example.com": {
    "paths": {
      "/example_redirect": {
        "path": "/temp_path",
        "active": true,
      }
    },
    "active": true,
  }
}
```

Redirecting paths within the same site using a HTTP 3xx redirect:

```JSON
{
  "example.com": {
    "paths": {
      "/example_redirect": {
        "path": "/temp_path",
        "status": 301,
        "active": true,
      }
    },
    "active": true,
  }
}
```

Redirecting paths from one site to another:

```JSON
{
  "example.com": {
    "host": "example2.com",
    "paths": {
      "/example_redirect": {
        "path": "/",
        "active": true,
      }
    },
    "active": true,
  }
}
```

This can also be done on a path by path basis:

```JSON
{
  "example.com": {
    "paths": {
      "host": "example2.com",
      "/example_redirect": {
        "path": "/",
        "active": true,
      },
      "/example_redirect2": {
        "host": "example3.com",
        "path": "/",
        "active": true,
      }
    },
    "active": true,
  }
}
```

If a host is configured for a path it takes precedence over the site redirect host.

Redirecting one domain to another:

```JSON
{
  "example.com": {
    "host": "example2.com",
    "active": true,
  }
}
```

This applies to all paths for the domain.


---

## Intercepting requests

### Intercept configuration

Parameters:

* Object key: String - Domain to Intercept.
* `active`: Boolean - True to enable proxy.
* `description`: String - [optional] A description for your proxy.

An example configuration file:

```JSON
{
  "example.com": {
    "active": true,
    "description": "Intercept & modify"
  }
}
```


---

## Proxying requests

Parameters:

* Object key: String - Domain to proxy.
* `active`: Boolean - True to enable proxy.
* `description`: String - [optional] A description for your proxy.

Proxy can be configured to either proxy all requests:

```JSON
{
  "*": {
    "active": true,
    "description": "Proxy All"
  }
}
```

or specific domains only:

```JSON
{
  "example.com": {
    "active": true,
    "description": "Proxy example.com"
  }
}
```


---

## Wildcards

The '\*' character can be used as a wildcard.

### Domain wildcards

```*.example.com``` will handle requests for all subdomains, but not ```example.com```.
```*example.com``` will handle requests for all subdomains, including ```example.com```.

In the following example the first configuration ```example.com``` will only proxy requests for ```example.com```.
While the second configuration ```\*.example.com``` will proxy all subdomains but not ```example.com```.

```JSON
{
  "example.com": {
    "active": true,
    "description": "Proxy example.com"
  },
  "*.example.com": {
    "active": true,
    "description": "Proxy subdomains of example.com"
  }
}
```

This snippet can be simplified to:

```JSON
{
  "*example.com": {
    "active": true,
    "description": "Proxy example.com and all subdomains"
  }
}
```


### Path wildcards (Only available for redirects)

```/testing/*``` will redirect all requests for path ```/testing``` including sub paths i.e ```/testing/path_a```

In the following example ```example.com/example_redirect``` and all sub paths will be redirected to ```example.com/temp_path```.

```JSON
{
  "example.com": {
    "paths": {
      "/example_redirect/*": {
        "path": "/temp_path",
        "active": true,
      }
    },
    "active": true,
  }
}
```


