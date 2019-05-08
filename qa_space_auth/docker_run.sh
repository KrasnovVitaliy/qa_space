#!/usr/bin/env bash
docker run -v `pwd`/qa_space_auth:/db/ -p 7000:7000 qa_space_auth