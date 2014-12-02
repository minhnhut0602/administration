#!/usr/bin/python
#
# (c) 2014 jw@owncloud.com
# Distribute under GPLv2 or ask.
#
# obs_docker_install.py -- prepare a docker image with owncloud packages
# V0.1 -- jw	initial draught, with APT only.
# V0.2 -- jw	support for extra-packages added, support for YUM, ZYPP added.
#               support debian packages without release number

from argparse import ArgumentParser
import json, sys, os, re, time
import subprocess, urllib2, base64


__VERSION__="0.2"
target="xUbuntu_14.04"

default_obs_config = {
  "_comment": "Written by "+sys.argv[0]+" -- edit also the builtin template",
  "obs":
    {
      "https://api.opensuse.org":
	{
	  "aliases": ["obs"],
	  "prj_re": "^(isv:ownCloud:|home:jnweiger)",
	  "download": 
	    { 
	      "public":   "http://download.opensuse.org/repositories/", 
	    },
	},
    },
  "target":
    {
      "xUbuntu_14.10":   { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"ubuntu:14.10" },
      "xUbuntu_14.04":   { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"ubuntu:14.04" },
      "xUbuntu_13.10":   { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"ubuntu:13.10" },
      "xUbuntu_13.04":   { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"ubuntu:13.04" },
      "xUbuntu_12.10":   { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"ubuntu:12.10" },
      "xUbuntu_12.04":   { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"ubuntu:12.04" },
      "Debian_6.0":      { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"debian:6.0" },
      "Debian_7.0":      { "fmt":"APT", "pre": ["wget","apt-transport-https"], "from":"debian:7" },

      "CentOS_7":        { "fmt":"YUM", "pre": ["wget"], "from":"centos:centos7" },
      "CentOS_6":        { "fmt":"YUM", "pre": ["wget"], "from":"centos:centos6" },
      "CentOS_CentOS-6": { "fmt":"YUM", "pre": ["wget"], "from":"centos:centos6" },
      "Fedora_20":       { "fmt":"YUM", "pre": ["wget"], "from":"fedora:20" },
      "openSUSE_13.2":   { "fmt":"ZYPP", "from":"opensuse:13.2" },
      "openSUSE_13.1":   { "fmt":"ZYPP", "from":"opensuse:13.1" }
    }
}

docker_volumes=[]

################################################################################

# Keep in sync with docker_install_oc.py
def run(args, input=None, redirect=None, redirect_stdout=True, redirect_stderr=True, return_tuple=False, tee=False):
  """
     make the subprocess monster usable
  """

  if redirect is not None:
    redirect_stderr = redirect
    redirect_stdout = redirect

  if redirect_stderr:
    redirect_stderr=subprocess.PIPE
  else:
    redirect_stderr=sys.stderr

  if redirect_stdout:
    redirect_stdout=subprocess.PIPE
  else:
    redirect_stdout=sys.stdout

  in_redirect=""
  in_fd=None
  if input is not None:
    in_fd = subprocess.PIPE
    in_redirect=" (<< '%s')" % input

  print "+ %s%s" % (args, in_redirect)
  p = subprocess.Popen(args, stdin=in_fd, stdout=redirect_stdout, stderr=redirect_stderr)
 
  (out,err) = p.communicate(input=input)

  if tee:
    if tee == True: tee=sys.stdout
    if out: print >>tee, " "+ out
    if err: print >>tee, " STDERROR: " + err

  if return_tuple: return (out,err)
  if err and out: return out + "\nSTDERROR: " + err
  if err: return "STDERROR: " + err
  return out

def urlopen_auth(url, username, password):
  request = urllib2.Request(url)
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)
  return urllib2.urlopen(request)


def check_dependencies():
  docker_bin = run(["which", "docker"], redirect_stderr=False)
  if not re.search("/docker", docker_bin, re.S):
    print """docker not installed? Try:
 sudo zypper in docker
"""
    sys.exit(0)
  docker_pid = run(["pidof", "docker"], redirect_stderr=False)
  if not re.search("\d\d+", docker_pid, re.S):
    print """docker is not running? Try:
 sudo systemctl enable docker
 sudo systemctl start docker
"""
    sys.exit(0)
  docker_grp = run(["id", "-a"], redirect_stderr=False)
  if not re.search("docker", docker_grp, re.S):
    print """You are not in the docker group? Try:
 sudo usermod -a -G docker $USER; reboot"
"""
    sys.exit(0)


def guess_obs_api(prj, override=None):
  if override:
    for obs in obs_config['obs']:
      if override == obs:
        return obs
      o=obs_config['obs'][obs]
      if o.has_key('aliases'):
        for a in o['aliases']:
          if override == a:
            print "guess_obs_api: alias="+a+" -> "+obs
	    return obs
    print "Warning: obs_api="+override+" not found in "+args.configfile
    return override	# not found.
  # actual guesswork
  for obs in obs_config['obs']:
    o=obs_config['obs'][obs]
    if o.has_key('prj_re') and re.match(o['prj_re'], prj):
      print "guess_obs_api: prj="+prj+" -> "+obs
      return obs
  raise ValueError("guess_obs_api failed for project='"+prj+"', try different project, -A, or update config in "+args.configfile)

def obs_fetch_bin_version(api, prj, pkg, target):
  bin_seen = run(["osc", "-A"+api, "ls", "-b", args.project, args.package, target])
  # cernbox-client_1.7.0-0.jw20141127_amd64.deb
  m = re.search('^\s*'+re.escape(args.package)+'_(\d+[^-\s]+)\-(\d+[^_\s]+)_.*?\.deb$', bin_seen, re.M)
  if m: return (m.group(1),m.group(2))
  # owncloud-client_1.7.0_i386.deb
  m = re.search('^\s*'+re.escape(args.package)+'_(\d+[^_\s]+)_.*?\.deb$', bin_seen, re.M)
  if m: return (m.group(1),'')

  # cloudtirea-client-1.7.0-4.1.i686.rpm
  m = re.search('^\s*'+re.escape(args.package)+'-(\d+[^-\s]+)\-([\w\.]+?)\.(x86_64|i\d86|noarch)\.rpm$', bin_seen, re.M)
  if m: return (m.group(1),m.group(2))
  raise ValueError("package for "+target+" not seen in 'osc ls -b' output: \n"+ bin_seen)


def docker_from_obs(obs_target_name):
  if obs_target_name in obs_config['target']:
    r = obs_config['target'][obs_target_name]
    r['obs'] = obs_target_name
    return r
  raise ValueError("no docker base image known for '"+obs_target_name+"' - choose other obs target or update config in "+args.configfile)

def obs_download(config, item, prj_path):
  """
    prj_path is appended to url_cred, where all ':' are replaced with ':/'
    a '/' is asserted between url_cred and prj_path.
    url_cred is guaranteed to end in '/'
    url, username, password, are derived from url_cred.

    Side-Effect:
      The resulting url_cred is tested, and a warning is printed, if it is not accessible.
  """
  if not config.has_key('download'):
    raise ValueError("obs_download: cannot read download url from config")
  if not config["download"].has_key(item):
    raise ValueError("obs_download: has no item '"+item+"' -- check --download option.")

  url_cred=config["download"][item]
  if not prj_path is None:
    if not re.search('/$', url_cred): url_cred += '/'
    url_cred += re.sub(':',':/',prj_path)
  if not re.search('/$', url_cred): url_cred += '/'
  data = { "url_cred":url_cred }

  # yet another fluffy url parser ahead
  m=re.match('(\w+://)([^/]+)(/.*)', url_cred)
  if m:
    # https://
    url_proto = m.group(1)
    # meself:pass1234@obs.owncloud.com:8888
    server_cred = m.group(2)
    # /path/where/...
    url_path = m.group(3)
    m=re.match('(.*)@(.*)$', server_cred)
    if m:
      # meself:pass1234
      cred = m.group(1)
      # obs.owncloud.com:8888
      server = m.group(2)
      m=re.match('(.*):(.*)', cred)
      if m:
        data['username'] = m.group(1)
	data['password'] = m.group(2)
      else:
        data['username'] = cred
      data['url'] = url_proto + server + url_path
    else:
      data['url'] = url_proto + server_cred + url_path
  else:
    data['url'] = url_cred	# oops.

  try:
    print "testing "+data['url']
    if data.has_key('username') and data.has_key('password'):
      uo = urlopen_auth(data['url'], data['username'], data['password'])
    else:
      uo = urllib2.urlopen(urllib2.Request(data['url']))
    text = uo.readlines()
    # print data['url'], "=>", text
  except Exception as e:
    print "WARNING: Cannot read "+data['url']+"\n"+str(e)
    print "\nTry a different --download option or wait 10 sec..."
    time.sleep(10)

  return data

################################################################################

ap = ArgumentParser(epilog="""Example:
 """+sys.argv[0]+""" isv:ownCloud:desktop/owncloud-client CentOS_CentOS-6

Version:
 """+__VERSION__, description="Create docker images for owncloud packages built with openSUSE Build Service (public or other instance).")
ap.add_argument("-p", "--platform", dest="target", metavar="TARGET", help="obs build target name. Default: "+target)
ap.add_argument("-f", "--from", metavar="IMG", help="docker base image to start with. Exclusive with specifying a -p platform name")
ap.add_argument("-V", "--version", default=False, action="store_true", help="print version number and exit")
ap.add_argument("-d", "--download", default='public', metavar="SERVER", help='use a different download server. Try "internal" or a full url. Default: "public"')
ap.add_argument("-c", "--configfile", default='obs_docker.json', metavar="FILE", help='specify different config file. Default: generate a default file if missing, so that you can edit')
ap.add_argument("-W", "--writeconfig", default=False, action="store_true", help='Write a default config file and exit. Default: use existing config file')
ap.add_argument("-A", "--obs-api", help="Identify the build service. Default: guessed from project name")
ap.add_argument("-n", "--image-name", help="Specify the name of the generated docker image. Default: construct a name and print")
ap.add_argument("-e", "--extra-packages", help="Comma separated list of packages to pre-install. Default: only per 'pre' in the config file")
ap.add_argument("-N", "--no-operation", default=False, action="store_true", help="Print docker commands to create an image only. Default: create an image")
ap.add_argument("-R", "--rm", default=False, action="store_true", help="Remove intermediate docker containers after a successful build")
ap.add_argument("--no-cache", default=False, action="store_true", help="Do not use cache when building the image. Default: use docker cache as available")
ap.add_argument("-X", "--xauth", default=False, action="store_true", help="Prepare a docker image that can connect to your X-Server.")
ap.add_argument("project", metavar="PROJECT", nargs="?", help="obs project name. Alternate syntax to PROJ/PACK")
ap.add_argument("package", metavar="PACKAGE",  nargs="?", help="obs package name, or PROJ/PACK")
ap.add_argument("platform",metavar="PLATFORM", nargs="?", help="obs build target name. Alternate syntax to -p. Default: "+target)
args = ap.parse_args() 	# --help is automatic

if args.version: ap.exit(__VERSION__)

if args.writeconfig:
  if os.path.exists(args.configfile):
    print "Will not overwrite existing "+args.configfile
    print "Please use -c to choose a different name, or move the file away"
    sys.exit(0)
  cfp = open(args.configfile, "w")
  json.dump(default_obs_config, cfp, indent=4, sort_keys=True)
  cfp.write("\n")
  cfp.close()
  print "default config written to " + args.configfile
  sys.exit(0)

if not os.path.exists(args.configfile):
  print "Config file does not exist: "+args.configfile
  print "Use -W to generate the file, or use -c to choose different config file"
  sys.exit()

if args.project is None:
  print "need project/package name"
  sys.exit(0)

m = re.match('(.*)/(.*)', args.project)
if m is None and args.package is None:
  print "need both, project and package"
  sys.exit(0)
if m:
  args.platform = args.package
  args.package = m.group(2)
  args.project = m.group(1)

if args.target:   target=args.target
if args.platform: target=args.platform
if args.target and args.platform:
  print "specify either a build target platform with -p or as a third parameter. Not both"
  sys.exit(0)
target = re.sub(':','_', target)	# just in case we get the project name instead of the build target name

cfp = open(args.configfile)

try:
  obs_config = json.load(cfp)
except Exception as e:
  print "ERROR: loading "+args.configfile+" failed: ", e
  print ""
  obs_config = default_obs_config

docker=docker_from_obs(target)
if not args.no_operation:
  check_dependencies()

obs_api=guess_obs_api(args.project, args.obs_api)
version,release=obs_fetch_bin_version(obs_api, args.project, args.package, target)

download=obs_download(obs_config["obs"][obs_api], args.download, args.project)

if args.image_name:
  image_name = args.image_name
else:
  image_name = args.package+'-'+version+'-'+release+'-'+docker['from']


if args.xauth:
  xauthdir="/tmp/.docker"
  xauthfile=xauthdir+"/wildcardhost.xauth"
  xa_cmd="xauth nlist :0 | sed -e 's/^0100/ffff/' | xauth -f '"+xauthfile+"' nmerge -"
  if not args.no_operation:
    run(["rm", "-rf", xauthdir])
    if not os.path.isdir(xauthdir): os.makedirs(xauthdir)	# mkdir -p $xauthdir
    open(xauthfile, "w").write("")				# touch $xauthfile
    run(["chgrp", "docker", xauthfile], redirect_stderr=False)
    run(["sh", "-c", xa_cmd], redirect_stderr=False)
    os.chmod(xauthfile, 0660)				# chmod 660 $xauthfile
  xsock="/tmp/.X11-unix"
  docker_volumes.append(xsock+':'+xsock)
  docker_volumes.append(xauthfile+':'+xauthfile)

docker_run=["docker","run","-ti"]
for vol in docker_volumes:
  docker_run.extend(["-v", vol])
docker_run.append(image_name)
print "#+ " + " ".join(docker_run)

dockerfile="FROM "+docker['from']+"\n"
dockerfile+="ENV TERM ansi\n"

wget_cmd="wget"
if download.has_key("username"): wget_cmd+=" --user '"+download["username"]+"'"
if download.has_key("password"): wget_cmd+=" --password '"+download["password"]+"'"
wget_cmd+=" "+download["url"]
if not re.search('/$', wget_cmd): wget_cmd+='/'

if docker["fmt"] == "APT":
  dockerfile+="RUN apt-get -y update\n"
  if docker.has_key("pre") and len(docker["pre"]):
    dockerfile+="RUN apt-get -y install "+" ".join(docker["pre"])+"\n"
  dockerfile+="RUN "+wget_cmd+target+"/Release.key\n"
  dockerfile+="RUN apt-key add - < Release.key\n"
  dockerfile+="RUN echo 'deb "+download["url_cred"]+"/"+target+"/ /' >> /etc/apt/sources.list.d/"+args.package+".list\n"
  dockerfile+="RUN apt-get -y update\n"
  if args.extra_packages:
    dockerfile+="RUN apt-get -y install "+re.sub(',',' ',args.extra_packages)+"\n"
  dockerfile+="RUN apt-get -y install "+args.package+" || true\n"
  dockerfile+="RUN echo 'apt-get install "+args.package+"' >> ~/.bash_history\n"
elif docker["fmt"] == "YUM":
  dockerfile+="RUN yum clean expire-cache\n" 
  if docker.has_key("pre") and len(docker["pre"]):
    dockerfile+="RUN yum install -y "+" ".join(docker["pre"])+"\n"
  dockerfile+="RUN "+wget_cmd+target+'/'+args.project+".repo -O /etc/yum.repos.d/"+args.project+".repo\n"
  if args.extra_packages:
    dockerfile+="RUN yum install -y "+re.sub(',',' ',args.extra_packages)+"\n"
  dockerfile+="RUN yum install -y "+args.package+" || true\n"
  dockerfile+="RUN echo 'yum install -y "+args.package+"' >> ~/.bash_history\n"
elif docker["fmt"] == "ZYPP":
  dockerfile+="RUN zypper --non-interactive "+download["url"]+target+"/"+args.project+".repo\n" 
  dockerfile+="RUN zypper --non-interactive --gpg-auto-import-keys refresh\n"
  if docker.has_key("pre") and len(docker["pre"]):
    dockerfile+="RUN zypper --non-interactive install "+" ".join(docker["pre"])+"\n"
  if args.extra_packages:
    dockerfile+="RUN uypper --non-interactive install "+re.sub(',',' ',args.extra_packages)+"\n"
  dockerfile+="RUN zypper --non-interactive install "+args.package+" || true\n"
  dockerfile+="RUN echo 'zypper install "+args.package+"' >> ~/.bash_history\n"
else:
  raise ValueError("dockerfile generator not implemented for fmt="+docker["fmt"])

if args.xauth:
  dockerfile+="ENV DISPLAY :0\n"
  dockerfile+="ENV XAUTHORITY "+xauthfile+"\n"
  dockerfile+='RUN : "'+xa_cmd+'"'+"\n"
dockerfile+='RUN : "'+" ".join(docker_run)+'"'+"\n"
dockerfile+="CMD /bin/bash\n"

# print obs_api, download, image_name, target, docker 
print dockerfile

if args.no_operation:
  print " - You can use the above Dockerfile to create an image like this:\n docker build -t "+image_name+" -\n"
else:
  docker_build=["docker", "build"]
  if args.rm: docker_build.append("--rm")
  if args.no_cache: docker_build.append("--no-cache")
  run(docker_build+["-t", image_name, "-"], input=dockerfile, redirect_stdout=False, redirect_stderr=False)  
  print "Image created. Check for errors in the above log.\n"
if not args.rm:
  print "Please remove intermediate images with e.g."
  print " docker ps -a | grep Exited | awk '{ print $1 }' | xargs docker rm\n"

print "You can run the new image with:\n "+" ".join(docker_run)