# Docker Remote

![](docs/logo.png) *Note: This is work in progress software.*

  [Compose]: https://github.com/docker/compose

Remote is a tool for managing Docker applications via [Compose] on another
machine. It uses SSH tunnels to connect your Docker and Docker Compose client
with your Docker Host.

    $ docker-remote shell
    Setting up a docker-compose alias...
    
    $ alias && echo $DOCKER_HOST
    alias docker-compose='docker-remote compose'
    tcp://localhost:2375
    $ cat docker-compose.yml
    version: '3.4'
    services:
      web:
        image: nginx
    x-docker-remote:
      project:
        name: myapp
    
    $ docker-compose up --build --detach
    $ docker ps

Check out the [Documentation](docs/) for installation instructions and
tutorials.

__Features__

* Allows you to compose and manage applications remotely
* Pre-processes your Docker Compose configuration in order to place all
  named and relative volume names inside a project directory.
* Ability to automatically add a `dockerhost` hostname to `/etc/hosts` for
  all or selected services

---

<p align="center">Copyright &copy; 2018 Niklas Rosenstein</p>
