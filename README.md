# Socio-Cognitive Engineering: Pepper Music Companion 🤖🎵

This repository is part of our group project for the Socio-Cognitive Engineering course (CS4235) at TU Delft, providing a demo of the humanoid robot [Pepper](https://www.aldebaran.com/en/pepper) as an interactive music companion for individuals with dementia.

## Overview 🌟
The goal of our project is to enhance the mental well-being and emotional comfort of individuals with dementia in care-homes, using the humanoid robot [Pepper](https://www.aldebaran.com/en/pepper) as interactive music companion.

This repository contains a small demo of Pepper's capability to interact with individuals, assess their mood through dialogue, and play music to enhance their comfort, taking into account their current emotional state. 

For more detailed information on our project's background, concept, and implementation, please refer to the documentation on our [XWiki](https://xwiki.ewi.tudelft.nl/xwiki/wiki/sce2024group02).

## Technology and Implementation 💻
For the development of our system, we used the [Social Interaction Cloud (SIC)](https://socialrobotics.atlassian.net/wiki/spaces/CBSR/overview) framework as basis. Our implemention for the demo can be found here: `framework/sic_framework/tests/mood_based_music_player.py`

We use the integration of [Google Dialogflow]() for intent management during the conversation.

### Setup 🛠

Install SIC framework following this OS-specific [install guide](https://socialrobotics.atlassian.net/wiki/spaces/CBSR/pages/2180415493/Install).

To get started with the robot, follow these instructions:

Navigate to the `framework` folder in your terminal and start redis:
```shell
redis-server conf/redis/redis.conf
```

Open a second terminal window to start the ```dialogflow.py``` service:
```shell
python3 sic_framework/services/dialogflow/dialogflow.py
```

Open a third terminal window to run our demo:
```shell
python3 sic_framework/tests/mood_based_music_player.py
```

### Error Management 🚨

#### Redis

If you encounter the error `Could not create server TCP listening socket *:6379: bind: Address already in use.`, please use the following command to stop the Redis server first:

Linux
`sudo systemctl stop redis-server.service`

MacOS
`sudo lsof -i :637`
`kill -9 PID` -> replace 'PID' with the process ID identied in the previous step


## Contributors 👥

- [Andy Huynh](https://github.com/Andyyh00)
- [Bugra Yildiz](https://github.com/bugrayildiz1)
- [Kenny Brandon](https://github.com/ramen4me)
- [Rutger Doting](https://github.com/RDoting)
- Tine Coutuer
- [Victoria Leskoschek](https://github.com/levichy)
