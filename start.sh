#!/bin/bash

export NODE_OPTIONS=--openssl-legacy-provider
sudo neo4j restart
cd crusoe_orient
npm run start &
cd ../graphql-api 
npm run start
