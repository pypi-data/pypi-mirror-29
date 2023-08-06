ts3ekkoutil
===========

A collection of utility methods and especially configuration options which are used in both, the ts3ekkoclient and ts3ekkomanage module.

Configuration Options
---------------------

Options can either be configured via app argument (``--ts3-server-host voice.teamspeak.com``) or environemnt variable (``export EKKO_TS3_SERVER_HOST=voice.teamspeak.com``).

Following options are available:

.. code-block::

  --ts3-server-host EKKO_TS3_SERVER_HOST
                        Hostname/ip of ts3 server
  --ts3-server-port EKKO_TS3_SERVER_PORT
                        Port of the ts3 server
  --ts3-username EKKO_TS3_USERNAME
                        Username of the bot
  --ts3-identity EKKO_TS3_IDENTITY
                        Identity to be used for the bot
  --ts3-unique-id EKKO_TS3_UNIQUEID
                        Unique ID, used to identify the bots own actions
  --ts3-client-apikey EKKO_TS3_CLIENT_APIKEY
                        ClientQuery apikey, configured in the ts3 client
                        docker image
  --ts3-channel-name EKKO_TS3_CHANNEL_NAME
                        Channel name to which the bot should connect
  --ts3-channel-id EKKO_TS3_CHANNEL_ID
                        Channel ID to which the bot should connect
  --ts3-channel-password EKKO_TS3_CHANNEL_PASSWORD
                        Channel password for the channel the bot is connecting
                        to
  --ts3-server-password EKKO_TS3_SERVER_PASSWORD
                        Password to the ts3 server
  --ts3-server-permission-token EKKO_TS3_SERVER_PERMISSION_TOKEN
                        Permission token to claim rights on the ts3 server.
  --ts3-identity-database-preconf EKKO_TS3_IDENTITY_DATABASE_PRECONF
                        Identity string which is pre-configured in the
                        ProtobufItems table in the settings.db inside of the
                        deployed client instance.
  --ts3-identity-database-key EKKO_TS3_IDENTITY_DATABASE_KEY
                        Identitfier key of the record in the ProtobufItems
                        table in the settings.db configuration database, which
                        should be used for the identity modification
  --ekko-node-id EKKO_NODE_ID
                        Identifier for each ekko client node
  --ts3-clientquery-host EKKO_TS3_CLIENTQUERY_HOST
                        Host used by the TS3 Client to provide the ClientQuery
                        endpoint
  --ts3-clientquery-port EKKO_TS3_CLIENTQUERY_PORT
                        Port used by the TS3 Client to provide the ClientQuery
                        endpoint
  --ts3-config-directory EKKO_TS3_CONFIG_DIRECTORY
                        Directory in which the TS3 configuration files are
                        (.ts3client, files are e.g. settings.db)
  --ekko-media-directory-source EKKO_MEDIA_DIRECTORY_SOURCE
                        Directory in which files for playback from filesystem
                        are stored on the docker host. This directory will be
                        mounted to the directory defined by `--ekko-media-
                        directory`.
  --ekko-media-directory EKKO_MEDIA_DIRECTORY
                        Directory in which files for playback from filesystem
                        are stored
  --teamspeak-directory EKKO_TS3_DIRECTORY
                        Directory in which teamspeak was installed
  --teamspeak-runscript EKKO_TS3_RUNSCRIPT
                        Filename of the runscript in the teamspeak directory
                        (see --teamspeak-directory)
  --docker-ekkoclient-build
                        Build the ekkoclient image instead of downloading the
                        built one
  --docker-ekkoclient-directory EKKO_DOCKER_EKKOCLIENT_DIRECTORY
                        Source directory for building the ekkoclient image
  --docker-network-name EKKO_DOCKER_NETWORK_NAME
                        Name of the docker network for the ekko ensamble.
  --docker-debug-diable-autoremove
                        Do not remove the containers of exited ekko clients
                        (only for debug purposes, results in errors in case
                        manager tries to create existing containers)
  --docker-ekkoclient-image-name EKKO_DOCKER_EKKOCLIENT_IMAGE_NAME
                        Name of the ekko client image
  --docker-ekkoclient-image-tag EKKO_DOCKER_EKKOCLIENT_IMAGE_TAG
                        Tag of the ekko client image
  --docker-network-dblink EKKO_DOCKER_NETWORK_DBLINK
                        Link descriptor for database<->ekkoclient link
  --ekko-client-control-port EKKO_CLIENT_CONTROL_PORT
                        Port on which the ekkoclients offer the control
                        service.
  --fixtures-path EKKO_FIXTURES_PATH
                        Path of the directory which includes seed/fixture
                        files for database initialization
  --db-username EKKO_DB_USERNAME
                        application database username
  --db-password EKKO_DB_PASSWORD
                        application database password
  --db-host EKKO_DB_HOST
                        application database host
  --db-dbname EKKO_DB_DBNAME
                        application database name
  --ekko-manage-server EKKO_MANAGE_SERVER
                        Hostname/ip of the server on which the ts3ekko
                        management instance runs
  --ekko-manage-port EKKO_MANAGE_PORT
                        Port on which the ts3ekko manage api can be reached
  --log-level EKKO_LOG_LEVEL
                        Log level for all ekko applications
  --log-format EKKO_LOG_FORMAT
                        Format in which the log messages are written
  --cog-media-volume-modifier EKKO_COG_MEDIA_VOLUME_MODIFIER
                        (MediaCog) Ratio by which the volume gets recalculated
                        for the media player.
  --cog-media-volume-max EKKO_COG_MEDIA_VOLUME_MAX
                        (MediaCog) Maximum allowed volume.
  --cog-media-alias-prefix EKKO_COG_MEDIA_ALIAS_PREFIX
                        (MediaCog) Prefix used to a mark media alias.
