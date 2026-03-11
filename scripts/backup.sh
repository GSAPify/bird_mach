#!/bin/bash
DATE=$(date +%Y%m%d)
pg_dump mach > backup_$DATE.sql
