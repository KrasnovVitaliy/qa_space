#!/usr/bin/env bash
docker run -v `pwd`/qa_space:/db/ -p 8080:8080 qa_space