# API

This container is a wrapper for REST APIs called from the [Grafana Dash](../dashboard/README.md).

The Grafana weather dashboard uses the [grafana-json-datasource](https://github.com/marcusolsson/grafana-json-datasource) to retrieve sunset and sunrise times.
The underlying REST API only returns times in GMT.
This container acts as wrapper for the sunrise API adjusting the times.

From the Balena point of view this container is the simplest.
The only thing to watch out for is that the container is configured to use the bridge network.
This means that the Sinatra app needs to be configured to bind to all interfaces:

```ruby
set :bind, '0.0.0.0'
```

Otherwise, Sinatra will only bind to the loopback interface, and you won't be able to access the API from outside the container.

## Configuration

This container makes use of three device service variables.
_LATITUDE_ the latitude value for the sunrise/sunset location, _LONGITUDE_ the longitude value for the sunrise/sunset location and _TIMEZONE_ for the timezone in which to display the times.

## Technologies

This container is implemented in Ruby based on a simple [Sinatra](http://sinatrarb.com/) app for serving the custom JSON APIs.

## Development

To run the API server locally, run:

```sh
bundle exec rake run
```

Copy _.template.env_ to _.env_ and adjust _LATITUDE_, _LONGITUDE_ and _TIMEZONE_ to match your location.

## Misc

* [Ruby API with Sinatra](https://x-team.com/blog/how-to-create-a-ruby-api-with-sinatra/)
* [Sunset and sunrise times API](https://sunrise-sunset.org/api)
