﻿# TOTALLY AWESOME KAFKA BATTLE SIMULATOR

## Purpose

A python based kafka demonstration in the form of a 'battle simulation' between a Hero and Enemy.

Hero and enemy will be separate containers and will use a kafka broker to consume
a new turn from a 'battle' main, then produce an action for that turn.

The 'battle' container will produce a new turn at the start of a battle and when it recieves
an action from both hero and enemy for the turn. It will then calculate each characters new health
based on damage from the action and produce a new turn if neither hero or enemy health drops below 0.

## To Run

Can be deployed locally in docker with:
docker-compose up
