<?php
// videogen config
// Env setup

define('WP_HOME','http://'.$_SERVER['HTTP_HOST']);
define('WP_SITEURL','http://'.$_SERVER['HTTP_HOST']);

// setup wp-memcached
$memcached_servers = array(
	'default' => array(
		'memcached:11211'
	)
);
define('ONDEMAND_CACHE' , true );

// No updates
define( 'WP_AUTO_UPDATE_CORE', false );
define( 'AUTOMATIC_UPDATER_DISABLED', true );

//  Allow plugins instal
define('FS_METHOD', 'direct');



/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', 'password');

/** MySQL hostname */
define('DB_HOST', 'mysql');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '27353c7265a93a9cd5658e25ac92d4dc85081eae');
define('SECURE_AUTH_KEY',  'c1ed60fbb9cb13de8334f08fc8a1c04cf9ecdf9a');
define('LOGGED_IN_KEY',    '90165910c2520b2ba5fea09c2b9ff032f76e16a6');
define('NONCE_KEY',        '8fb59827e38377fd055cf2b372e7a242082f84fe');
define('AUTH_SALT',        '2ba94c941dbab55ac60b3c365c10a2ac013895a4');
define('SECURE_AUTH_SALT', '8828a9bf9ab9e32f1cd859f1288fe0356f86bb36');
define('LOGGED_IN_SALT',   '72a738c1f9c599ae7e84213d20bf687891a29693');
define('NONCE_SALT',       '7a1f180d3920731e1d1f50de725729e475ad0868');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', true);
// tp debug queries
define( 'SAVEQUERIES', true );

// If we're behind a proxy server and using HTTPS, we need to alert Wordpress of that fact
// see also http://codex.wordpress.org/Administration_Over_SSL#Using_a_Reverse_Proxy
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
	$_SERVER['HTTPS'] = 'on';
}

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');