# modifying the dockerinit binary breaks the SHA1 sum check by docker
%global __os_install_post %{_rpmconfigdir}/brp-compress

#debuginfo not supported with Go
%global debug_package %{nil}
%global gopath  %{_datadir}/gocode

%global import_path github.com/docker/docker
%global commit   dc45aa10f1033f7a0f1a995a78b8f92540c34fc2
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           docker
Version:        1.2.0
Release:        15%{?dist}
Summary:        Automates deployment of containerized applications
License:        ASL 2.0

URL:            http://www.docker.io
# only x86_64 for now: https://github.com/docker/docker/issues/136
ExclusiveArch:  x86_64
Source0:        https://github.com/rhatdan/docker/archive/%{commit}/docker-%{shortcommit}.tar.gz
Patch1: docker-version.patch
Patch2: Add-registry-append-and-registry-replace-qualifier-t.patch
# though final name for sysconf/sysvinit files is simply 'docker',
# having .sysvinit and .sysconfig makes things clear
Source1:        docker.service
Source2:        docker-man-3.tar.gz
Source3:        docker.sysconfig
# docker: systemd socket activation results in privilege escalation
Source4:        docker.socket
Source5:        codegansta.tgz
BuildRequires:  gcc
BuildRequires:  glibc-static
# ensure build uses golang 1.2-7 and above
# http://code.google.com/p/go/source/detail?r=a15f344a9efa35ef168c8feaa92a15a1cdc93db5
BuildRequires:  golang >= 1.3.1
BuildRequires:  golang(github.com/gorilla/mux) >= 0-0.12
BuildRequires:  golang(github.com/kr/pty) >= 0-0.20
BuildRequires:  golang(code.google.com/p/go.net/websocket)
BuildRequires:  golang(code.google.com/p/gosqlite/sqlite3)
BuildRequires:  golang(github.com/syndtr/gocapability/capability) >= 0-0.6
BuildRequires:  golang(github.com/godbus/dbus)
BuildRequires:  golang(github.com/coreos/go-systemd/activation) >= 2-2
#BuildRequires:  golang(github.com/codegangsta/cli)
BuildRequires:  device-mapper-devel
BuildRequires:  btrfs-progs-devel
BuildRequires:  pkgconfig(systemd)
Requires:       systemd-units
# need xz to work with ubuntu images
Requires:       xz

Provides:       lxc-docker = %{version}
Provides:       docker
Provides:	docker-io
Provides:       nsinit

%description
Docker is an open-source engine that automates the deployment of any
application as a lightweight, portable, self-sufficient container that will
run virtually anywhere.

Docker containers can encapsulate any payload, and will run consistently on
and between virtually any server. The same container that a developer builds
and tests on a laptop will run at scale, in production*, on VMs, bare-metal
servers, OpenStack clusters, public instances, or combinations of the above.

%package devel
BuildRequires:  golang
Summary:        A golang registry for global request variables (source libraries)
Provides:       docker-pkg-devel docker-io-pkg-devel
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/api) = %{version}-%{release}
Provides:       golang(%{import_path}/api/client) = %{version}-%{release}
Provides:       golang(%{import_path}/api/server) = %{version}-%{release}
Provides:       golang(%{import_path}/archive) = %{version}-%{release}
Provides:       golang(%{import_path}/builtins) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/docker-device-tool) = %{version}-%{release}
Provides:       golang(%{import_path}/contrib/host-integration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/execdrivers) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/lxc) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native/configuration) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/execdriver/native/template) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/aufs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/btrfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/devmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/graphtest) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/graphdriver/vfs) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/bridge) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/ipallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portallocator) = %{version}-%{release}
Provides:       golang(%{import_path}/daemon/networkdriver/portmapper) = %{version}-%{release}
Provides:       golang(%{import_path}/dockerversion) = %{version}-%{release}
Provides:       golang(%{import_path}/engine) = %{version}-%{release}
Provides:       golang(%{import_path}/graph) = %{version}-%{release}
Provides:       golang(%{import_path}/image) = %{version}-%{release}
Provides:       golang(%{import_path}/integration) = %{version}-%{release}
Provides:       golang(%{import_path}/integration-cli) = %{version}-%{release}
Provides:       golang(%{import_path}/links) = %{version}-%{release}
Provides:       golang(%{import_path}/nat) = %{version}-%{release}
Provides:       golang(%{import_path}/opts) = %{version}-%{release}
Provides:       golang(%{import_path}/registry) = %{version}-%{release}
Provides:       golang(%{import_path}/runconfig) = %{version}-%{release}
Provides:       golang(%{import_path}/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/utils/broadcastwriter) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/graphdb) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/iptables) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/listenbuffer) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mflag/example) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/mount) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/namesgenerator) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/etchosts) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/networkfs/resolvconf) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/signal) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/symlink) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/sysinfo) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/system) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/systemd) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/tailfile) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/term) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/testutils) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/truncindex) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/units) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/user) = %{version}-%{release}
Provides:       golang(%{import_path}/pkg/version) = %{version}-%{release}

Obsoletes:	golang-github-docker-libcontainer-devel

%description devel
This is the source libraries for docker.

%prep
%setup -q -n docker-%{commit}
%patch1 -p1 -b .version
%patch2 -p1 -b .registry
tar zxf %{SOURCE2} 
tar zxf %{SOURCE5} 

%build
mkdir _build

pushd _build
  mkdir -p src/github.com/docker
  ln -s $(dirs +1 -l) src/github.com/docker/docker
popd

export DOCKER_GITCOMMIT="%{shortcommit}/%{version}"
export DOCKER_BUILDTAGS='selinux'
export GOPATH=$(pwd)/_build:$(pwd)/vendor:%{gopath}

hack/make.sh dynbinary
cp contrib/syntax/vim/LICENSE LICENSE-vim-syntax
cp contrib/syntax/vim/README.md README-vim-syntax.md

#build nsinit
pushd $(pwd)/_build/src
  go build github.com/docker/libcontainer/nsinit
popd

%install
# install binary
install -d %{buildroot}%{_bindir}
install -p -m 755 bundles/%{version}/dynbinary/docker-%{version} %{buildroot}%{_bindir}/docker

# install dockerinit
install -d %{buildroot}%{_libexecdir}/docker
install -p -m 755 bundles/%{version}/dynbinary/dockerinit-%{version} %{buildroot}%{_libexecdir}/docker/dockerinit

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 man1/* %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man5
install -p -m 644 man5/* %{buildroot}%{_mandir}/man5

# install bash completion
install -d %{buildroot}%{_datadir}/bash-completion/completions/
install -p -m 644 contrib/completion/bash/docker %{buildroot}%{_datadir}/bash-completion/completions/

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 contrib/completion/zsh/_docker %{buildroot}%{_datadir}/zsh/site-functions

# install vim syntax highlighting
install -d %{buildroot}%{_datadir}/vim/vimfiles/{doc,ftdetect,syntax}
install -p -m 644 contrib/syntax/vim/doc/dockerfile.txt %{buildroot}%{_datadir}/vim/vimfiles/doc
install -p -m 644 contrib/syntax/vim/ftdetect/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect
install -p -m 644 contrib/syntax/vim/syntax/dockerfile.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

# install udev rules
install -d %{buildroot}%{_sysconfdir}/udev/rules.d
install -p -m 755 contrib/udev/80-docker.rules %{buildroot}%{_sysconfdir}/udev/rules.d

# install storage dir
install -d -m 700 %{buildroot}%{_sharedstatedir}/docker

# install systemd/init scripts
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE4} %{buildroot}%{_unitdir}
# for additional args
install -d %{buildroot}%{_sysconfdir}/sysconfig/
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/docker

# install secrets dir
install -d -p -m 750 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/rhel7.repo

mkdir -p %{buildroot}/etc/docker/certs.d/redhat.com
ln -s /etc/rhsm/ca/redhat-uep.pem %{buildroot}/etc/docker/certs.d/redhat.com/redhat-ca.crt

# Install nsinit
install -d -p %{buildroot}%{gopath}/src/github.com/docker/libcontainer/nsinit
cp -pav vendor/src/github.com/docker/libcontainer/nsinit/*.go %{buildroot}%{gopath}/src/github.com/docker/libcontainer/nsinit
install -d %{buildroot}%{_bindir}
install -p -m 755 ./_build/src/nsinit %{buildroot}%{_bindir}/nsinit

# Install libcontainer
for dir in . apparmor cgroups cgroups/fs cgroups/systemd \
	console devices label mount mount/nodes namespaces \
	netlink network nsinit security/capabilities \
	security/restrict selinux syncpipe system user utils
do
    install -d -p %{buildroot}%{gopath}/src/github.com/docker/libcontainer/$dir
    cp -pav vendor/src/github.com/docker/libcontainer/$dir/*.go %{buildroot}%{gopath}/src/github.com/docker/libcontainer/$dir
done

# sources
install -d -p %{buildroot}/%{gopath}/src/%{import_path}

for dir in api archive builtins daemon dockerversion engine graph \
           image links nat opts pkg registry runconfig utils
do
       echo $dir
        cp -pav $dir %{buildroot}/%{gopath}/src/%{import_path}/
done
find %{buildroot}/%{gopath}/src/%{import_path}/ -name \*.registry -delete

%pre
getent group docker > /dev/null || %{_sbindir}/groupadd -r docker
exit 0

%post
%systemd_post docker

%preun
%systemd_preun docker

%postun
%systemd_postun_with_restart docker

%files
%defattr(-,root,root,-)
%doc AUTHORS CHANGELOG.md CONTRIBUTING.md MAINTAINERS NOTICE
%doc LICENSE* README*.md
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_bindir}/docker
%dir %{_datadir}/rhel
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/etc-pki-entitlement
%{_datadir}/rhel/secrets/rhel7.repo
%{_datadir}/rhel/secrets/rhsm
%dir %{_libexecdir}/docker
%{_libexecdir}/docker/dockerinit
%{_unitdir}/docker.service
%{_unitdir}/docker.socket
%config(noreplace) %{_sysconfdir}/sysconfig/docker
%{_sysconfdir}/docker/certs.d
#%{_sysconfdir}/docker/certs.d/redhat.com
#%{_sysconfdir}/docker/certs.d/redhat.com/redhat-ca.crt
%{_datadir}/bash-completion/completions/docker
%{_datadir}/zsh/site-functions/_docker
%dir %{_sharedstatedir}/docker
%dir %{_sysconfdir}/udev/rules.d
%{_sysconfdir}/udev/rules.d/80-docker.rules
%dir %{_datadir}/vim/vimfiles/doc
%{_datadir}/vim/vimfiles/doc/dockerfile.txt
%dir %{_datadir}/vim/vimfiles/ftdetect
%{_datadir}/vim/vimfiles/ftdetect/dockerfile.vim
%dir %{_datadir}/vim/vimfiles/syntax
%{_datadir}/vim/vimfiles/syntax/dockerfile.vim
%{_bindir}/nsinit
%dir %{gopath}/src/github.com/docker/libcontainer/nsinit
%{gopath}/src/github.com/docker/libcontainer/nsinit/*.go
%dir %{gopath}/src/%{import_path}/runconfig
%{gopath}/src/%{import_path}/runconfig/*.go
%dir %{gopath}/src/%{import_path}/utils
%{gopath}/src/%{import_path}/utils/*.go

%files devel
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path}/api
%{gopath}/src/%{import_path}/api/MAINTAINERS
%{gopath}/src/%{import_path}/api/README.md
%{gopath}/src/%{import_path}/api/*.go
%dir %{gopath}/src/%{import_path}/api/client
%{gopath}/src/%{import_path}/api/client/*.go
%dir %{gopath}/src/%{import_path}/api/server
%{gopath}/src/%{import_path}/api/server/MAINTAINERS
%{gopath}/src/%{import_path}/api/server/*.go
%dir %{gopath}/src/%{import_path}/archive
%{gopath}/src/%{import_path}/archive/MAINTAINERS
%{gopath}/src/%{import_path}/archive/README.md
%{gopath}/src/%{import_path}/archive/*.go
%dir %{gopath}/src/%{import_path}/archive/testdata
%{gopath}/src/%{import_path}/archive/testdata/broken.tar
%dir %{gopath}/src/%{import_path}/builtins
%{gopath}/src/%{import_path}/builtins/*.go
%dir %{gopath}/src/%{import_path}/daemon
%{gopath}/src/%{import_path}/daemon/*.go
%{gopath}/src/%{import_path}/daemon/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/README.md
%dir %{gopath}/src/%{import_path}/daemon/execdriver
%{gopath}/src/%{import_path}/daemon/execdriver/*.go
%{gopath}/src/%{import_path}/daemon/execdriver/MAINTAINERS
%dir %{gopath}/src/%{import_path}/daemon/execdriver/execdrivers
%{gopath}/src/%{import_path}/daemon/execdriver/execdrivers/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/lxc
%{gopath}/src/%{import_path}/daemon/execdriver/lxc/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/execdriver/lxc/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/native
%{gopath}/src/%{import_path}/daemon/execdriver/native/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/native/configuration
%{gopath}/src/%{import_path}/daemon/execdriver/native/configuration/*.go
%dir %{gopath}/src/%{import_path}/daemon/execdriver/native/template
%{gopath}/src/%{import_path}/daemon/execdriver/native/template/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver
%{gopath}/src/%{import_path}/daemon/graphdriver/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/aufs
%{gopath}/src/%{import_path}/daemon/graphdriver/aufs/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/btrfs
%{gopath}/src/%{import_path}/daemon/graphdriver/btrfs/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/btrfs/MAINTAINERS
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/devmapper
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/*.go
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/MAINTAINERS
%{gopath}/src/%{import_path}/daemon/graphdriver/devmapper/README.md
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/graphtest
%{gopath}/src/%{import_path}/daemon/graphdriver/graphtest/*.go
%dir %{gopath}/src/%{import_path}/daemon/graphdriver/vfs
%{gopath}/src/%{import_path}/daemon/graphdriver/vfs/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/bridge
%{gopath}/src/%{import_path}/daemon/networkdriver/bridge/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/ipallocator
%{gopath}/src/%{import_path}/daemon/networkdriver/ipallocator/*.go
%{gopath}/src/%{import_path}/daemon/networkdriver/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/portallocator
%{gopath}/src/%{import_path}/daemon/networkdriver/portallocator/*.go
%dir %{gopath}/src/%{import_path}/daemon/networkdriver/portmapper
%{gopath}/src/%{import_path}/daemon/networkdriver/portmapper/*.go
%dir %{gopath}/src/%{import_path}/dockerversion
%{gopath}/src/%{import_path}/dockerversion/*.go
%dir %{gopath}/src/%{import_path}/engine
%{gopath}/src/%{import_path}/engine/MAINTAINERS
%{gopath}/src/%{import_path}/engine/*.go
%dir %{gopath}/src/%{import_path}/graph
%{gopath}/src/%{import_path}/graph/MAINTAINERS
%{gopath}/src/%{import_path}/graph/*.go
%dir %{gopath}/src/%{import_path}/image
%{gopath}/src/%{import_path}/image/*.go
%dir %{gopath}/src/%{import_path}/links
%{gopath}/src/%{import_path}/links/*.go
%dir %{gopath}/src/%{import_path}/nat
%{gopath}/src/%{import_path}/nat/*.go
%dir %{gopath}/src/%{import_path}/opts
%{gopath}/src/%{import_path}/opts/*.go
%dir %{gopath}/src/%{import_path}/registry
%{gopath}/src/%{import_path}/registry/MAINTAINERS
%{gopath}/src/%{import_path}/registry/*.go
%dir %{gopath}/src/%{import_path}/runconfig
%{gopath}/src/%{import_path}/runconfig/*.go
%dir %{gopath}/src/%{import_path}/utils
%{gopath}/src/%{import_path}/utils/*.go
#libcontainer
%dir %{gopath}/src/github.com/docker/libcontainer
%dir %{gopath}/src/github.com/docker/libcontainer/apparmor
%dir %{gopath}/src/github.com/docker/libcontainer/cgroups
%dir %{gopath}/src/github.com/docker/libcontainer/cgroups/fs
%dir %{gopath}/src/github.com/docker/libcontainer/cgroups/systemd
%dir %{gopath}/src/github.com/docker/libcontainer/console
%dir %{gopath}/src/github.com/docker/libcontainer/devices
%dir %{gopath}/src/github.com/docker/libcontainer/label
%dir %{gopath}/src/github.com/docker/libcontainer/mount
%dir %{gopath}/src/github.com/docker/libcontainer/mount/nodes
%dir %{gopath}/src/github.com/docker/libcontainer/namespaces
%dir %{gopath}/src/github.com/docker/libcontainer/netlink
%dir %{gopath}/src/github.com/docker/libcontainer/network
%dir %{gopath}/src/github.com/docker/libcontainer/nsinit
%dir %{gopath}/src/github.com/docker/libcontainer/security
%dir %{gopath}/src/github.com/docker/libcontainer/security/capabilities
%dir %{gopath}/src/github.com/docker/libcontainer/security/restrict
%dir %{gopath}/src/github.com/docker/libcontainer/selinux
%dir %{gopath}/src/github.com/docker/libcontainer/syncpipe
%dir %{gopath}/src/github.com/docker/libcontainer/system
%dir %{gopath}/src/github.com/docker/libcontainer/user
%dir %{gopath}/src/github.com/docker/libcontainer/utils
%{gopath}/src/github.com/docker/libcontainer/*.go
%{gopath}/src/github.com/docker/libcontainer/apparmor/*.go
%{gopath}/src/github.com/docker/libcontainer/cgroups/*.go
%{gopath}/src/github.com/docker/libcontainer/cgroups/fs/*.go
%{gopath}/src/github.com/docker/libcontainer/cgroups/systemd/*.go
%{gopath}/src/github.com/docker/libcontainer/console/*.go
%{gopath}/src/github.com/docker/libcontainer/devices/*.go
%{gopath}/src/github.com/docker/libcontainer/label/*.go
%{gopath}/src/github.com/docker/libcontainer/mount/*.go
%{gopath}/src/github.com/docker/libcontainer/mount/nodes/*.go
%{gopath}/src/github.com/docker/libcontainer/namespaces/*.go
%{gopath}/src/github.com/docker/libcontainer/netlink/*.go
%{gopath}/src/github.com/docker/libcontainer/network/*.go
%{gopath}/src/github.com/docker/libcontainer/nsinit/*.go
%{gopath}/src/github.com/docker/libcontainer/security/capabilities/*.go
%{gopath}/src/github.com/docker/libcontainer/security/restrict/*.go
%{gopath}/src/github.com/docker/libcontainer/selinux/*.go
%{gopath}/src/github.com/docker/libcontainer/syncpipe/*.go
%{gopath}/src/github.com/docker/libcontainer/system/*.go
%{gopath}/src/github.com/docker/libcontainer/user/*.go
%{gopath}/src/github.com/docker/libcontainer/utils/*.go

%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path}/pkg
%{gopath}/src/%{import_path}/pkg/README.md
%dir %{gopath}/src/%{import_path}/pkg/broadcastwriter
%{gopath}/src/%{import_path}/pkg/broadcastwriter/*.go
%dir %{gopath}/src/%{import_path}/pkg/graphdb
%{gopath}/src/%{import_path}/pkg/graphdb/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/graphdb/*.go
%dir %{gopath}/src/%{import_path}/pkg/httputils
%{gopath}/src/%{import_path}/pkg/httputils/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/httputils/*.go
%dir %{gopath}/src/%{import_path}/pkg/iptables
%{gopath}/src/%{import_path}/pkg/iptables/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/iptables/*.go
%dir %{gopath}/src/%{import_path}/pkg/jsonlog
%{gopath}/src/%{import_path}/pkg/jsonlog/*.go
%dir %{gopath}/src/%{import_path}/pkg/listenbuffer
%{gopath}/src/%{import_path}/pkg/listenbuffer/*.go
%dir %{gopath}/src/%{import_path}/pkg/log
%{gopath}/src/%{import_path}/pkg/log/*.go
%dir %{gopath}/src/%{import_path}/pkg/mflag
%{gopath}/src/%{import_path}/pkg/mflag/LICENSE
%{gopath}/src/%{import_path}/pkg/mflag/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/mflag/README.md
%dir %{gopath}/src/%{import_path}/pkg/mflag/example
%{gopath}/src/%{import_path}/pkg/mflag/example/example.go
%{gopath}/src/%{import_path}/pkg/mflag/*.go
%dir %{gopath}/src/%{import_path}/pkg/mount
%{gopath}/src/%{import_path}/pkg/mount/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/mount/*.go
%dir %{gopath}/src/%{import_path}/pkg/namesgenerator
%{gopath}/src/%{import_path}/pkg/namesgenerator/*.go
%dir %{gopath}/src/%{import_path}/pkg/networkfs
%{gopath}/src/%{import_path}/pkg/networkfs/MAINTAINERS
%dir %{gopath}/src/%{import_path}/pkg/networkfs/etchosts
%{gopath}/src/%{import_path}/pkg/networkfs/etchosts/*.go
%dir %{gopath}/src/%{import_path}/pkg/networkfs/resolvconf
%{gopath}/src/%{import_path}/pkg/networkfs/resolvconf/*.go
%dir %{gopath}/src/%{import_path}/pkg/parsers
%{gopath}/src/%{import_path}/pkg/parsers/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/parsers/*.go
%dir %{gopath}/src/%{import_path}/pkg/parsers/filters
%{gopath}/src/%{import_path}/pkg/parsers/filters/*.go
%dir %{gopath}/src/%{import_path}/pkg/parsers/kernel
%{gopath}/src/%{import_path}/pkg/parsers/kernel/*.go
%dir %{gopath}/src/%{import_path}/pkg/parsers/operatingsystem
%{gopath}/src/%{import_path}/pkg/parsers/operatingsystem/*.go
%dir %{gopath}/src/%{import_path}/pkg/proxy
%{gopath}/src/%{import_path}/pkg/proxy/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/proxy/*.go
%dir %{gopath}/src/%{import_path}/pkg/signal
%{gopath}/src/%{import_path}/pkg/signal/*.go
%dir %{gopath}/src/%{import_path}/pkg/symlink
%{gopath}/src/%{import_path}/pkg/symlink/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/symlink/*.go
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata/fs
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/d
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/e
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/a/f
%dir %{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/b
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/b/h
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/g
%{gopath}/src/%{import_path}/pkg/symlink/testdata/fs/i
%dir %{gopath}/src/%{import_path}/pkg/sysinfo
%{gopath}/src/%{import_path}/pkg/sysinfo/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/sysinfo/*.go
%dir %{gopath}/src/%{import_path}/pkg/system
%{gopath}/src/%{import_path}/pkg/system/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/system/*.go
%dir %{gopath}/src/%{import_path}/pkg/systemd
%{gopath}/src/%{import_path}/pkg/systemd/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/systemd/*.go
%dir %{gopath}/src/%{import_path}/pkg/tailfile
%{gopath}/src/%{import_path}/pkg/tailfile/*.go
%dir %{gopath}/src/%{import_path}/pkg/tarsum
%{gopath}/src/%{import_path}/pkg/tarsum/*.go
%{gopath}/src/%{import_path}/pkg/tarsum/MAINTAINER
%dir %{gopath}/src/%{import_path}/pkg/tarsum/testdata
%dir %{gopath}/src/%{import_path}/pkg/tarsum/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457
%{gopath}/src/%{import_path}/pkg/tarsum/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457/json
%{gopath}/src/%{import_path}/pkg/tarsum/testdata/46af0962ab5afeb5ce6740d4d91652e69206fc991fd5328c1a94d364ad00e457/layer.tar
%dir %{gopath}/src/%{import_path}/pkg/tarsum/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158
%{gopath}/src/%{import_path}/pkg/tarsum/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/json
%{gopath}/src/%{import_path}/pkg/tarsum/testdata/511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158/layer.tar
%dir %{gopath}/src/%{import_path}/pkg/truncindex
%{gopath}/src/%{import_path}/pkg/truncindex/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/truncindex/*.go
%dir %{gopath}/src/%{import_path}/pkg/term
%{gopath}/src/%{import_path}/pkg/term/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/term/*.go
%dir %{gopath}/src/%{import_path}/pkg/testutils
%{gopath}/src/%{import_path}/pkg/testutils/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/testutils/README.md
%{gopath}/src/%{import_path}/pkg/testutils/utils.go
%dir %{gopath}/src/%{import_path}/pkg/units
%{gopath}/src/%{import_path}/pkg/units/MAINTAINERS
%{gopath}/src/%{import_path}/pkg/units/*.go
%dir %{gopath}/src/%{import_path}/pkg/version
%{gopath}/src/%{import_path}/pkg/version/*.go
%dir %{gopath}/src/%{import_path}/pkg/ioutils
%{gopath}/src/%{import_path}/pkg/ioutils/*.go
%dir %{gopath}/src/%{import_path}/pkg/pools
%{gopath}/src/%{import_path}/pkg/pools/*.go

%changelog
* Wed Sep 17 2014 Tomas Hrcka <thrcka@redhat.com> - 1.2.0-15
- Add provides docker-io to get through compatibility issues

* Tue Sep 16 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-14
- Add registry-append and registry-replace patch

* Mon Sep 15 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-13
- Fix Comment and META patch to work in Dockerfile

* Fri Sep 12 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-12
- Update man pages

* Fri Sep 12 2014 Tomas Hrcka <thrcka@redhat.com> - 1.2.0-11
- Add missing pieces of libcontainer
- Devel now obsoletes golang-github-docker-libcontainer-devel

* Thu Sep 11 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-10
- Re-add all of the patches

* Thu Sep 11 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-9
- Remove runtime dependency on golang

* Thu Sep 11 2014 Tomas Hrcka <thrcka@redhat.com> - 1.2.0-8
- Remove runtime dependency on golang

* Tue Sep 09 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-7
- Fix secrets patch

* Tue Sep 09 2014 Tomas Hrcka <thrcka@redhat.com> - 1.2.0-4
- Add -devel -pkg-devel subpackages
- Move libcontainer from -lib to -devel subpackage

* Mon Sep 08 2014 Dan Walsh <dwalsh@redhat.com> - 1.2.0-3
- Allow docker to use /etc/pki/entitlement for certs

* Mon Sep 08 2014 Tomas Hrcka <thrcka@redhat.com> - 1.2.0-2
- Enable nsinit again
- New sources that satisfy nsinit deps

* Thu Sep 04 2014 Tomas Hrcka <thrcka@redhat.com> - 1.2.0-1
- Bump release to 1.2.0
- Change docker client certs links
- Add nsinit
- Add docker-lib subpackage which provides libcontainer sources

* Tue Sep 2 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-10
- Add  docker client entitlement certs

* Fri Aug 8 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-9
- Add Matt Heon patch to allow containers to work if machine is not entitled

* Thu Aug 7 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-8
- Fix handing of rhel repos

* Mon Aug 4 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-6
- Update man pages

* Mon Jul 28 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-5
- Fix environment patch
- Add /etc/machine-id patch

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-4
- Add Secrets Patch back in

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-3
- Pull in latest docker-1.1.2 code

* Fri Jul 25 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.2-2
- Update to the latest from upstream
- Add comment and envoroment patches to allow setting of comments and 
- enviroment variables from docker import

* Wed Jul 23 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-3
- Install docker bash completions in proper location
- Add audit_write as a default capability

* Tue Jul 22 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-2
- Update man pages
- Fix docker pull registry/repo

* Fri Jul 18 2014 Dan Walsh <dwalsh@redhat.com> - 1.1.1-1
- Update to latest from upstream

* Mon Jul 14 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-10
- Pass otions from /etc/sysconfig/docker into docker.service unit file

* Thu Jul 10 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-9
- Fix docker-registry patch to handle search

* Thu Jul 10 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-8
- Re-add %{_datadir}/rhel/secrets/rhel7.repo

* Wed Jul 9 2014 Dan Walsh <dwalsh@redhat.com> - 1.0.0-7
- Patch: Save "COMMENT" field in Dockerfile into image content.
- Patch: Update documentation noting that SIGCHLD is not proxied.
- Patch: Escape control and nonprintable characters in docker ps
- Patch: machine-id: add container id access
- Patch: Report child error better (and later)
- Patch: Fix invalid fd race
- Patch: Super minimal host based secrets
- Patch: libcontainer: Mount cgroups in the container
- Patch: pkg/cgroups Add GetMounts() and GetAllSubsystems()
- Patch: New implementation of /run support
- Patch: Error if Docker daemon starts with BTRFS graph driver and SELinux enabled
- Patch: Updated CLI documentation for docker pull with notes on specifying URL
- Patch: Updated docker pull manpage to reflect ability to specify URL of registry.
- Patch: Docker should use /var/tmp for large temporary files.
- Patch: Add --registry-append and --registry-replace qualifier to docker daemon
- Patch: Increase size of buffer for signals
- Patch: Update documentation noting that SIGCHLD is not proxied.
- Patch: Escape control and nonprintable characters in docker ps

* Tue Jun 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-4
- Documentation update for --sig-proxy
- increase size of buffer for signals
- escape control and nonprintable characters in docker ps

* Tue Jun 24 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-3
- Resolves: rhbz#1111769 - CVE-2014-3499

* Thu Jun 19 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-2
- Resolves: rhbz#1109938 - upgrade to upstream version 1.0.0 + patches
  use repo: https://github.com/lsm5/docker/commits/htb2
- Resolves: rhbz#1109858 - fix race condition with secrets
- add machine-id patch:
https://github.com/vbatts/docker/commit/4f51757a50349bbbd2282953aaa3fc0e9a989741

* Wed Jun 18 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.0.0-1
- Resolves: rhbz#1109938 - upgrade to upstream version 1.0.0 + patches
  use repo: https://github.com/lsm5/docker/commits/2014-06-18-htb2
- Resolves: rhbz#1110876 - secrets changes required for subscription
management
- btrfs now available (remove old comment)

* Fri Jun 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-19
- build with golang-github-kr-pty-0-0.19.git98c7b80.el7

* Fri Jun 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-18
- update manpages
- use branch: https://github.com/lsm5/docker/commits/2014-06-06-2

* Thu Jun 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-17
- use branch: https://github.com/lsm5/docker/commits/2014-06-05-final2

* Thu Jun 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-16
- latest repo: https://github.com/lsm5/docker/commits/2014-06-05-5
- update secrets symlinks

* Mon Jun 02 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-15
- correct the rhel7.repo symlink

* Mon Jun 02 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-14
- only symlink the repo itself, not the dir

* Sun Jun 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-13
- use the repo dir itself and not repo for second symlink

* Sat May 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-12
- create symlinks at install time and not in scriptlets
- own symlinks in /etc/docker/secrets

* Sat May 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-11
- add symlinks for sharing host entitlements

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-10
- /etc/docker/secrets has permissions 750

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-9
- create and own /etc/docker/secrets

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-8
- don't use docker.sysconfig meant for sysvinit (just to avoid confusion)

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-7
- install /etc/sysconfig/docker for additional args
- use branch 2014-05-29 with modified secrets dir path

* Thu May 29 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-6
- secret store patch

* Thu May 22 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-5
- native driver: add required capabilities (dotcloud issue #5928)

* Thu May 22 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-4
- branch 2014-05-22
- rename rhel-dockerfiles dir to dockerfiles

* Wed May 21 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-3
- mount /run with correct selinux label

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-2
- add btrfs

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.11.1-1
- use latest master
- branch: https://github.com/lsm5/docker/commits/2014-05-09-2

* Mon May 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-13
- add registry search list patch

* Wed May 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-12
- include dockerfiles for postgres, systemd/{httpd,mariadb}

* Mon May 12 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-11
- add apache, mariadb and mongodb dockerfiles
- branch 2014-05-12

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-10
- add rhel-dockerfile/mongodb

* Fri May 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-9
- use branch: https://github.com/lsm5/docker/commits/2014-05-09
- install rhel-dockerfile for apache
- cleanup: get rid of conditionals
- libcontainer: create dirs/files as needed for bind mounts

* Thu May 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-8
- fix docker top

* Tue May 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-7
- set container pid for process in native driver

* Tue May 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-6
- ensure upstream PR #5529 is included

* Mon May 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-5
- block push to docker index

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-4
- enable selinux in unitfile

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-3
- branch https://github.com/lsm5/docker/commits/2014-05-01-2

* Thu May 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-2
- branch https://github.com/lsm5/docker/tree/2014-05-01

* Fri Apr 25 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.10.0-1
- renamed (docker-io -> docker)
- rebased on 0.10.0
- branch used: https://github.com/lsm5/docker/tree/2014-04-25
- manpages packaged separately (pandoc not available on RHEL-7)

* Tue Apr 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-4.collider
- manpages merged, some more patches from alex

* Thu Apr 03 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-3.collider
- fix --volumes-from mount failure, include docker-images/info/tag manpages

* Tue Apr 01 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-2.collider
- solve deadlock issue

* Mon Mar 31 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.1-1.collider
- branch 2014-03-28, include additional docker manpages from whenry

* Thu Mar 27 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-7.collider
- env file support (vbatts)

* Mon Mar 17 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-6.collider
- dwalsh's selinux patch rewritten
- point to my docker repo as source0 (contains all patches already)
- don't require tar and libcgroup

* Fri Mar 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-5.collider
- add kraman's container-pid.patch

* Fri Mar 14 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-4.collider
- require docker.socket in unitfile

* Thu Mar 13 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-3.collider
- use systemd socket activation

* Wed Mar 12 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-2.collider
- add collider tag to release field

* Tue Mar 11 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.9.0-1
- upstream version bump to 0.9.0

* Mon Mar 10 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-3
- add alexl's patches upto af9bb2e3d37fcddd5e041d6ae45055f649e2fbd4
- add guelfey/go.dbus to BR

* Sun Mar 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-2
- use upstream commit 3ace9512bdf5c935a716ee1851d3e636e7962fac
- add dwalsh's patches for selinux, emacs-gitignore, listen_pid and
remount /var/lib/docker as --private

* Wed Feb 19 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.1-1
- Bug 1066841 - upstream version bump to v0.8.1
- use sysvinit files from upstream contrib
- BR golang >= 1.2-7

* Thu Feb 13 2014 Adam Miller <maxamillion@fedoraproject.org> - 0.8.0-3
- Remove unneeded sysctl settings in initscript
  https://github.com/dotcloud/docker/pull/4125

* Sat Feb 08 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-2
- ignore btrfs for rhel7 and clones for now
- include vim syntax highlighting from contrib/syntax/vim

* Wed Feb 05 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.8.0-1
- upstream version bump
- don't use btrfs for rhel6 and clones (yet)

* Mon Jan 20 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-2
- bridge-utils only for rhel < 7
- discard freespace when image is removed

* Thu Jan 16 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.6-1
- upstream version bump v0.7.6
- built with golang >= 1.2

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.5-1
- upstream version bump to 0.7.5

* Thu Jan 09 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.4-1
- upstream version bump to 0.7.4 (BZ #1049793)
- udev rules file from upstream contrib
- unit file firewalld not used, description changes

* Mon Jan 06 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-3
- udev rules typo fixed (BZ 1048775)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-2
- missed commit value in release 1, updated now
- upstream release monitoring (BZ 1048441)

* Sat Jan 04 2014 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.3-1
- upstream release bump to v0.7.3

* Thu Dec 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-2
- require xz to work with ubuntu images (BZ #1045220)

* Wed Dec 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.2-1
- upstream release bump to v0.7.2

* Fri Dec 06 2013 Vincent Batts <vbatts@redhat.com> - 0.7.1-1
- upstream release of v0.7.1

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-14
- sysvinit patch corrected (epel only)
- 80-docker.rules unified for udisks1 and udisks2

* Mon Dec 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-13
- removed firewall-cmd --add-masquerade

* Sat Nov 30 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-12
- systemd for fedora >= 18
- firewalld in unit file changed from Requires to Wants
- firewall-cmd --add-masquerade after docker daemon start in unit file
  (Michal Fojtik <mfojtik@redhat.com>), continue if not present (Michael Young
  <m.a.young@durham.ac.uk>)
- 80-docker.rules included for epel too, ENV variables need to be changed for
  udisks1

* Fri Nov 29 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-11
- Redirect docker log to /var/log/docker (epel only)
- Removed the '-b none' parameter from sysconfig, it's unnecessary since
  we create the bridge now automatically (epel only)
- Make sure we have the cgconfig service started before we start docker,
    RHBZ#1034919 (epel only)

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-10
- udev rules added for fedora >= 19 BZ 1034095
- epel testing pending

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-9
- requires and started after firewalld

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-8
- iptables-fix patch corrected

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-7
- use upstream tarball and patch with mgoldman's commit

* Thu Nov 28 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-6
- using mgoldman's shortcommit value 0ff9bc1 for package (BZ #1033606)
- https://github.com/dotcloud/docker/pull/2907

* Wed Nov 27 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7.0-5
- Fix up EL6 preun/postun to not fail on postun scripts

* Wed Nov 27 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7.0-4
- brctl patch for rhel <= 7

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-3
- Patch how the bridge network is set up on RHEL (BZ #1035436)

* Wed Nov 27 2013 Vincent Batts <vbatts@redhat.com> - 0.7.0-2
- add libcgroup require (BZ #1034919)

* Tue Nov 26 2013 Marek Goldmann <mgoldman@redhat.com> - 0.7.0-1
- Upstream release 0.7.0
- Using upstream script to build the binary

* Mon Nov 25 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.20.rc7
- correct the build time defines (bz#1026545). Thanks dan-fedora.

* Fri Nov 22 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.7-0.19.rc7
- Remove xinetd entry, added sysvinit

* Fri Nov 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.18.rc7
- rc version bump

* Wed Nov 20 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.17.rc6
- removed ExecStartPost lines from docker.service (BZ #1026045)
- dockerinit listed in files

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.16.rc6
- adding back the none bridge patch

* Wed Nov 20 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.15.rc6
- update docker source to crosbymichael/0.7.0-rc6
- bridge-patch is not needed on this branch

* Tue Nov 19 2013 Vincent Batts <vbatts@redhat.com> - 0.7-0.14.rc5
- update docker source to crosbymichael/0.7-rc5
- update docker source to 457375ea370a2da0df301d35b1aaa8f5964dabfe
- static magic
- place dockerinit in a libexec
- add sqlite dependency

* Sat Nov 02 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.13.dm
- docker.service file sets iptables rules to allow container networking, this
    is a stopgap approach, relevant pull request here:
    https://github.com/dotcloud/docker/pull/2527

* Sat Oct 26 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.12.dm
- dm branch
- dockerinit -> docker-init

* Tue Oct 22 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.11.rc4
- passing version information for docker build BZ #1017186

* Sat Oct 19 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.10.rc4
- rc version bump
- docker-init -> dockerinit
- zsh completion script installed to /usr/share/zsh/site-functions

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.9.rc3
- lxc-docker version matches package version

* Fri Oct 18 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.8.rc3
- double quotes removed from buildrequires as per existing golang rules

* Fri Oct 11 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.7.rc3
- xinetd file renamed to docker.xinetd for clarity

* Thu Oct 10 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.6.rc3
- patched for el6 to use sphinx-1.0-build

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.5.rc3
- rc3 version bump
- exclusivearch x86_64

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.4.rc2
- debuginfo not Go-ready yet, skipped

* Wed Oct 09 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-0.3.rc2
- debuginfo package generated
- buildrequires listed with versions where needed
- conditionals changed to reflect systemd or not
- docker commit value not needed
- versioned provides lxc-docker

* Mon Oct 07 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-2.rc2
- rc branch includes devmapper
- el6 BZ #1015865 fix included

* Sun Oct 06 2013 Lokesh Mandvekar <lsm5@redhat.com> - 0.7-1
- version bump, includes devicemapper
- epel conditionals included
- buildrequires sqlite-devel

* Fri Oct 04 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-4.devicemapper
- docker-io service enables IPv4 and IPv6 forwarding
- docker user not needed
- golang not supported on ppc64, docker-io excluded too

* Thu Oct 03 2013 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.6.3-3.devicemapper
- Docker rebuilt with latest kr/pty, first run issue solved

* Fri Sep 27 2013 Marek Goldmann <mgoldman@redhat.com> - 0.6.3-2.devicemapper
- Remove setfcap from lxc.cap.drop to make setxattr() calls working in the
  containers, RHBZ#1012952

* Thu Sep 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.3-1.devicemapper
- version bump
- new version solves docker push issues

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-14.devicemapper
- package requires lxc

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-13.devicemapper
- package requires tar

* Tue Sep 24 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-12.devicemapper
- /var/lib/docker installed
- package also provides lxc-docker

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-11.devicemapper
- better looking url

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-10.devicemapper
- release tag changed to denote devicemapper patch

* Mon Sep 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-9
- device-mapper-devel is a buildrequires for alex's code
- docker.service listed as a separate source file

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-8
- install bash completion
- use -v for go build to show progress

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-7
- build and install separate docker-init

* Sun Sep 22 2013 Matthew Miller <mattdm@fedoraproject.org> 0.6.2-4
- update to use new source-only golang lib packages

* Sat Sep 21 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-3
- man page generation from docs/.
- systemd service file created
- dotcloud/tar no longer required

* Fri Sep 20 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-2
- patched with alex larsson's devmapper code

* Wed Sep 18 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.2-1
- Version bump

* Tue Sep 10 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-2
- buildrequires updated
- package renamed to docker-io
 
* Fri Aug 30 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.6.1-1
- Version bump
- Package name change from lxc-docker to docker
- Makefile patched from 0.5.3

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-5
- File permissions settings included

* Wed Aug 28 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-4
- Credits in changelog modified as per reference's request

* Tue Aug 27 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-3
- Dependencies listed as rpm packages instead of tars
- Install section added

* Mon Aug 26 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-2
- Github packaging
- Deps not downloaded at build time courtesy Elan Ruusamäe
- Manpage and other docs installed

* Fri Aug 23 2013 Lokesh Mandvekar <lsm5@redhat.com> 0.5.3-1
- Initial fedora package
- Some credit to Elan Ruusamäe (glen@pld-linux.org)
