from supportal.fabric_contrib import *

@task
def apt_postgresql():
    sources = "/etc/apt/sources.list.d/postgresql.list"
    if exists(sources):
        sudo("rm -f %s" % sources)
    append(sources, "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main", use_sudo=True)

    run("wget https://www.postgresql.org/media/keys/ACCC4CF8.asc")
    sudo("apt-key add ACCC4CF8.asc")
    sudo("apt-get update")
    sudo("apt-get install -y postgresql-9.4 postgresql-server-dev-9.4 libpq-dev")
    sudo("wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem -O /etc/ssl/certs/rds-combined-ca-bundle.pem")


@task
def brew_postgresql():
    if "postgresql" not in run("brew list"):
        run("brew install postgresql")
    run("mkdir -p ~/Library/LaunchAgents")
    run("ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents")
    if not exists("/usr/local/var/postgres"):
        run("initdb /usr/local/var/postgres")
    launchctl_reload("~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist")

@task
def osx():
    homebrew()
    brew_postgresql()
    drop_postgres_databases()
    create_postgres_role()
    create_postgres_databases()


@task
def ubuntu():
    apt_postgresql()
    drop_postgres_databases(use_sudo=True)
    create_postgres_role(use_sudo=True)
    create_postgres_databases(use_sudo=True)


def psql(command, use_sudo=False):
    from functools import partial
    func = partial(sudo, user='postgres') if use_sudo else run
    func('psql postgres --command="%s";' % command)


@task
def create_postgres_databases(use_sudo=False):
    psql("CREATE DATABASE postgres", use_sudo=use_sudo)
    if env.host == 'localhost':
        write_settings_py()

@task
def create_postgres_role(use_sudo=False):
    psql("CREATE ROLE postgres LOGIN PASSWORD 'postgres' SUPERUSER INHERIT CREATEDB CREATEROLE REPLICATION", use_sudo=use_sudo)


@task
def drop_postgres_databases(use_sudo=False):
    with settings(warn_only=True):
        psql("SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'postgres' AND pid <> pg_backend_pid();", use_sudo=use_sudo)
        psql("DROP DATABASE IF EXISTS postgres", use_sudo=use_sudo)
        psql("DROP ROLE IF EXISTS postgres", use_sudo=use_sudo)
