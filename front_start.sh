#!/bin/bash

export NODE_OPTIONS=--openssl-legacy-provider
cd crusoe_orient
npm run start &
cd ../graphql-api 
npm run start
