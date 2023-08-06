# uWebSockets Python Bindings [#25](https://github.com/uNetworking/bindings/pull/25)

 * These bindings are on [PyPi](https://pypi.python.org/pypi/uWebSockets) for Python 2.7 and Python 3.6
 * `pip2 install uWebSockets` or `pip3 install uWebSockets`

## Development

### Linux x86_64
 * For C/I there is a Dockerfile which will build a debian image. 
   * If you have debian/ubuntu you can just install the packages in that Dockerfile.
   * The Dockerfile is setup to work with Vagrant and there is a wildcard `vagrant/%` target in the Makefile
   * `make vagrant/wheels` or natively:
 * `make wheels`
 
### Windoze
 * Install [MSYS2](http://www.msys2.org/)
   * Then install python2 and python3 development libraries and openssl
     `pacman -S gcc g++ make msys/openssl-devel msys/libuv-devel python2 python3 msys/python2-pip msys/python3-pip`
 * `make wheels`

### OSX
 * 
 
 
## Complaints/Support
 * See [#25](https://github.com/uNetworking/bindings/pull/25)
 * Report issues with Python bindings to @szmoore
