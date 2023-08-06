# contents


### application (app) generation 

- app: prototype application
- create_app: script to create an app

### library routines

- lib: library routines, including data types  
- data: database interface
- render: .evo html templating
- serve: application server

### evoke classes for use in apps

- security classes
  - User: 
  - Reset:
  - Permit:
  - Session:
- foundation classes
  - Page: page hierarchy, including image and file handling
  - Var.py: system variables

### application support

- evo: default system-wide templates
- site: flat file resources common to all apps 

### system configuration

 - config_base.py: defaults
 - config_site.py: overrides for this server
 - config_multi.py: multi-app server config (see below)

### multi-app server (optional, as apps may be run individually)

 - devstart: development start script (runs in foreground) 
 - start: production start script (runs in background)
 - stop: production stop script
 - multiserve.py: twisted application - called by the above scripts
