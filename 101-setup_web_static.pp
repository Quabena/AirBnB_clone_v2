# Puppet manifest to set up web servers for web_static deployment

# Ensure Nginx is installed and running
package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}

# Create necessary directories with proper ownership
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  recurse => true,
}

# Create the fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => "<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>",
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
}

# Create or update the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true, # Ensures the link is recreated if it already exists
}

# Update Nginx configuration to serve content
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => template('setup_web_static/nginx_default.erb'),
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  notify  => Service['nginx'], # Restart Nginx after updating config
}

# Restart Nginx to apply changes
exec { 'reload-nginx':
  command     => '/etc/init.d/nginx reload',
  refreshonly => true,
  subscribe   => File['/etc/nginx/sites-available/default'],
}

