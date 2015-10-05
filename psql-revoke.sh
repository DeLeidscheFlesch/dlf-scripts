# Simpel script om privileges van een gebruiker op een database-schema in 
# PostgreSQL te verwijderen. Verandert eigenaar van objecten naar 'admin'
# 
# Gebruik: ./psql-revoke.sh database schema gebruiker
#
# Werkt niet voor
# -Grants die door een andere gebruiker dan postgres zijn gedaan. Hiervoor 
#  moet de GRANT OPTION van de betreffende gebruiker worden verwijderd
# -Eigendom van databases
# -Eigendom van views (geen syntax voor ALL VIEWS IN)

psql_exec()
{
        sudo -u postgres psql -U postgres $1 -c "${2}";
}

psql_reassign() 
{
        psql_exec $1 "REASSIGN OWNED BY ${2} to ${3}";
}

psql_revoke() 
{
        psql_exec $1 "REVOKE ALL PRIVILEGES ON ${2} FROM ${3} CASCADE;"
}

psql_reassign "${1}" "${3}" admin
psql_revoke "${1}" "ALL TABLES IN SCHEMA ${2}" "${3}"
psql_revoke "${1}" "ALL SEQUENCES IN SCHEMA ${2}" "${3}"
psql_revoke "${1}" "SCHEMA ${2}" "${3}"
psql_revoke "${1}" "DATABASE ${1}" "${3}"
