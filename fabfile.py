from fabric.api import env , run as myrun , put
from fabric.operations import local as localrun
# Declaration variables
env.devport = 80
env.pmaport = 9898
env.name = "local"
env.project= "travel"
env.user= "travel"
env.prod_domain = "fr.travel.com"
env.prod_srv = "srv.travel.fr"
env.preprod = "XX.XX.XX.XX"
env.prod = "XX.XX.XX.XX"

env.repo = "git@XX.XXX.XXX.XXX"

env.data_dir = "."
env.use_ssh_config = True

def preprod():
	env.hosts=[ env.preprod ]
	env.home="/home/travel"
	env.deploy_dir="/home/travel/travel-fr"
	env.data_dir="/home/travel/data"
	env.http_port=9888


def prod():
	env.hosts=[ env.prod ]
	env.home="/home/travel"
	env.deploy_dir="/home/travel/travel"
	env.data_dir="/home/travel/data"
	env.memcached="127.0.0.1:11211"

def clone():
	myrun("cd %s && git clone %s"  % ( env.home , env.repo ))

def update():
	myrun("cd %s && git pull -r"  % ( env.deploy_dir  ))

def update_config():
	myrun("cd %s && "  % ( env.deploy_dir  ))


def start(action='rebuild'):
    if action=='rebuild':
        command= 'up -d --build'
    else:
        command=action
    myrun("cd %s &&  SRCDIR=. DATADIR=%s  HTTPPORT=%s HTTPPORTPMA=8888 docker-compose -p %s %s"   %  ( env.deploy_dir , env.data_dir , env.http_port , env.project , command ))


def qa(action='start'):
    if action=='start':
        command= 'up -d'
    else:
        command=action

    localrun("SRCDIR=. DATADIR=%s  HTTPPORT=%d HTTPPORTPMA=%d docker-compose -p %s %s" %  ( env.data_dir, env.devport , env.pmaport , env.project , command )  )

def sync_down():
	localrun("rsync -rtv root@%s:/data/%s/data/data/ data/" %  (env.preprod , env.project )   )

def sync_up():
	localrun("rsync -rtv data/ root@%s:%s/data/" % (env.preprod , env.data_dir )  )

def sync_up_uploads():
	localrun("rsync -rtv data/uploads/ root@%s:/data/%s/data/data/uploads/" % (env.preprod , env.project )  )

def run_prod():
	localrun("SRCDIR=. DATADIR=.  HTTPPORT=80 HTTPPORTPMA=8888 docker-compose -p %s up -d"   % env.project )


def sync_down_prod():
	localrun("rsync -rtv root@%s:/home/%s/%s/data/ data/"   % (  env.prod_domain  , env.project , env.project )   )


# Avant de charge la base, la copier dans data/uploads/
def load_db_dump(file = 'dump'):
	localrun("docker exec %s_mysql_1 bash -c 'mysql -uroot -ppassword wordpress < /var/www/html/wp-content/uploads/%s.sql'" %  ( env.project , file  ) ) 



# Avant de charge la base, la copier dans data/uploads/
def save_db_dump():
	localrun("docker exec %s_mysql_1 mysqldump -uroot -ppassword wordpress > /var/www/html/wp-content/uploads/dump.sql" %  env.project)


def mysql():
	myrun("docker exec -ti %s_mysql_1 mysql -A -uroot -ppassword wordpress" %  env.project )

def localmysql():
	localrun("docker exec -ti %s_mysql_1 mysql  -A -uroot -ppassword wordpress" %  env.project )

def cli(command='sync'):
	localrun("docker exec -ti travel_web_1 wp --allow-root %s" % command )

# Install frensh lang
# fab cli:"language core install fr_FR --activate"
# fab cli:"language plugin install woocommerce fr_FR" 
# fab cli:"language plugin install woocommerce-admin fr_FR"
# fab cli:"language plugin install woocommerce-gateway-stripe fr_FR"
#  fab cli:"language plugin install woocommerce-services fr_FR" 

# Just remove wp-config.php before running this command
# Will create a new config file, then upgrade wordpress , user should commit the changes
def cli_upgrade():
	docker_command = "docker run -it --rm -v $(pwd):/var/www/html --network travel_default wordpress:cli wp"
	localrun("%s config create --dbname=wordpress --dbuser=root --dbpass=password --dbprefix=hml_  --dbhost=mysql" % docker_command )
	localrun("%s core update" % docker_command )
	localrun("%s core update-db" % docker_command )

def cli_plugin(plugin='--all'):
	docker_command = "docker run -it --rm -v $(pwd):/var/www/html --network travel_default wordpress:cli wp"
	localrun("%s plugin update %s" %  ( docker_command , plugin))



# In case of sync db
# docker exec -ti travel_mysql_1 mysql -uroot -ppassword wordpress
# update hml_options set option_value='http://localhost:9888/' where option_name = 'home' or option_name = 'siteurl' ;

# preprod
# update hml_options set option_value='http://5.196.70.66:9888/' where option_name = 'home' or option_name = 'siteurl' ;

# prod
# update hml_options set option_value='http://fr.travel.com/' where option_name = 'home' or option_name = 'siteurl' ;


def link_data():
	myrun("ln -fs %s/uploads %s/wp-content/uploads" % ( env.data_dir , env.deploy_dir ) )

def sync_up_prod_uploads():
	localrun("rsync -rtv data/uploads/ %s@%s:%s/uploads/" % ( env.user, env.prod , env.data_dir )  )

def sync_down_prod_uploads():
	localrun("rsync -rtv %s@%s:%s/uploads/ data/uploads/" % ( env.user, env.prod , env.data_dir )  )



def prepare_conf(password="test" ):
	myrun("ln -sf %s/wp-content/plugins/memcached-redux/object-cache.php %s/wp-content/object-cache.php" % ( env.deploy_dir , env.deploy_dir ))
	process_template("wp-config.prod.php" , "wp-config.php" , { 'PASSWORD' : password , 'MEMCACHED_URI' : env.memcached } )
	put( "wp-config.php" , "%s/wp-config.php" % env.deploy_dir  )

def process_template(template , output , context ):
	import os
	basename = os.path.basename(template)
	output = open(output, "w+b")
	# Init
	text = None

	with open(template) as inputfile:
		text = inputfile.read()

	if context:
		text = text % context
	#print " processed \n : %s" % text
	output.write(text)
	output.close()

def update_cron():
	#myrun("cd %s/cron && chmod +x sync*" % env.deploy_dir )
	process_template("cron-sample" , "cron-tab" , { 'DEPLOY_DIR' : env.deploy_dir , 'HOME_DIR' : env.home } )
	put( "cron-tab" , "%s/cron/cron-tab" % env.deploy_dir  )
	myrun("crontab %s/cron/cron-tab" % env.deploy_dir )

def send_cert():
	localrun("ssh %s@%s mkdir -p %s/cert && scp cert/* %s@%s:%s/cert" % ( env.user, env.prod, env.deploy_dir, env.user, env.prod, env.deploy_dir) )

def flash_http_cache():
	myrun("sudo rm -r -f /dev/shm/fastcgi_temp ")
	myrun("sudo rm -r -f /dev/shm/fastcgi_cache ")
	myrun("sudo systemctl reload nginx")

def flash_memcache():
	myrun("sudo systemctl restart memcached")
