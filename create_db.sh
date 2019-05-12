#!/usr/bin/env bash

#!/bin/bash
set -e

/etc/init.d/postgresql start
createdb qa_space_auth
/etc/init.d/postgresql stop