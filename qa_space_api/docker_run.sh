#!/usr/bin/env bash
docker run -v `pwd`/qa_space_api:/db/ -p 7080:7080 qa_space_api