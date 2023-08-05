# Centos-Package-Cron

[![Build Status](http://img.shields.io/travis/wied03/centos-package-cron/master.svg?style=flat)](http://travis-ci.org/wied03/centos-package-cron)
[![Quality](https://api.codeclimate.com/v1/badges/ce1d686b27f9ba2f4f2a/maintainability)](https://codeclimate.com/github/wied03/centos-package-cron/maintainability)

Attempts to offer Apticron (Ubuntu) style package update emails and also bring security notifications to CentOS via Meier's script

## What does it do?

* Checks for updates using Yum's Python API and changelogs for those updates using Yum's changelog plugin
* Checks security errata from CentOS mailing list via [Steve Meier's XML file](http://cefs.steve-meier.de/) and reports advisories related to packages installed on your machine
* Emails (or dumps to STDOUT) the above information to an address of your choosing
* By default, only reminds about a given security advisory / package update once to avoid annoying you.  You can change this using the --skipold false option (see -h)

## Why does this exist?

`yum --security` is an ideal solution, but it does not work on CentOS since the `updateinfo.xml` file in the CentOS repository does not include RHEL style security updates (see discussion [here](https://www.centos.org/forums/viewtopic.php?t=30967)). The options, which all depend on something like Steve's XML file (as of March 2016) that I know of are:

1. Use Spacewalk (see Steve site)
2. Generate `updateinfo.xml` with security information (see [VM farms post](http://blog.vmfarms.com/2013/12/inject-little-security-in-to-your.html))
3. This tool

Some of these are good options but if you don't want Spacewalk and want more Apticron/apt type features like the DB/remember piece, this might be a good option for you.

## Requirements

Tested on CentOS 7, 6.6, and 6.7, but coded in a way that should work even CentOS 5. The dependencies as listed in the RPM spec might need to be tweaked to run properly on CentOS < 6.6. If you can help test with that, feel free to create a pull request.

## Installation

### Using Python

From pypi:

```shell
# These packages are OS centric and not available on pypi
sudo yum install mailx yum-plugin-changelog
pip install centos_package_cron
# For the SQLite DB that avoids reminding you of updates that were already sent (see above)
mkdir /var/lib/centos-package-cron
```

From checked out copy:

```shell
sudo yum install mailx yum-plugin-changelog
./setup.py install
# For the SQLite DB that avoids reminding you of updates that were already sent (see above)
mkdir /var/lib/centos-package-cron
```

### Using RPM

You can download the source (or binary) RPM from the [releases page](https://github.com/wied03/centos-package-cron/releases).

**CentOS package submission pending**

OR if you want to build the RPM yourself:

If you use Docker, you can checkout this repository and build an RPM this way:

```shell
# install ruby & Rake
# use centos6 if that applies
CENTOS=centos7 rake build
# source and binary RPMs will be deposited in built_rpms directory
```

If you'd rather not use Docker or Ruby/Rake, then do something like this:
```shell
sudo yum install rpm-build yum-utils
# copy centos-package-cron.spec.in to centos-package-cron.spec and put the proper version numbers in those placeholders
sudo yum-builddep -y --disablerepo=updates centos-package-cron.spec
# Download a tar gzip of the source to /some/path/containing/source/centos_package_cron_src.tgz
rpmbuild -bb --verbose -D "_topdir `pwd`" -D "_sourcedir /some/path/containing/source" -D "_builddir `pwd`" centos-package-cron.spec
sudo yum install centos-package-cron-1.0.6-0.1.el7.centos.x86_64.rpm
```

## Usage

```shell
centos-package-cron --email_to sysadmin@stuff.com --email_from dev@somebox.com
# See centos-package-cron -h for options
```

NOTE: You must have an MTA (e.g. postfix) configured listening on localhost if you use the email output option.

## License
Copyright (c) 2016, BSW Technology Consulting LLC
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
