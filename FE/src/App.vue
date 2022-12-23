<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Loading from './components/Loading.vue'
import Recording from './components/Recording.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMicrophoneAlt, faStop } from '@fortawesome/free-solid-svg-icons'

library.add(faMicrophoneAlt, faStop)

const apiUrl = "https://voice-chatbot-api.saokhue.io"

const transcript = ref('')
const isRecording = ref(false)
const isLoading = ref(false)
const audio = ref();

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition
const sr = new Recognition()
sr.lang = 'vi-VN';

onMounted(() => {
	sr.continuous = true
	sr.interimResults = true

	sr.onstart = () => {
		isRecording.value = true
	}

	sr.onend = () => {
		isRecording.value = false
	}

	sr.onresult = (evt) => {
		for (let i = 0; i < evt.results.length; i++) {
			const result = evt.results[i]

			if (result.isFinal) CheckForCommand(result)
		}

		const t = Array.from(evt.results)
			.map(result => result[0])
			.map(result => result.transcript)
			.join('')
		
		transcript.value = t
	}
})

const CheckForCommand = () => {
  sr.stop()
  isLoading.value = true;
	axios
    .put(apiUrl + `/messages:input?text=${transcript.value}`)
    .then((response) => {
      if (response.status === 200) {
        transcript.value = response.data.text;
        transcript.value = transcript.value.replaceAll('- Bước', '\n - Bước')
        console.log(transcript.value);
        audio.value = new Audio("data:audio/mpeg;base64," + response.data.audio);
        audio.value.play();
      }
    }).finally(() => {
      isLoading.value = false;
    });
}

const ToggleMic = () => {
	if (isRecording.value) {
		sr.stop()
	} else {
    if (audio.value) {
      audio.value.pause();
    }
    audio.value = null;
		sr.start()
	}
}
</script>

<template>
	<div class="app">
    <Loading v-if="isLoading" class="f-center" />
    <Recording v-if="isRecording" class="f-center loading" />
    <div class="transcript"> {{ transcript }}</div>
    <div class="footer">
      <div class="micContainer" @click="ToggleMic">
        <div v-if="isRecording" class="btn">
          <font-awesome-icon icon="fa-solid fa-stop" />
        </div>
        <div v-else class="btn">
          <font-awesome-icon icon="fa-solid fa-microphone-alt" />
        </div>
      </div>
    </div>
	</div>
</template>

<style lang="scss">
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
	font-family: 'Fira sans', sans-serif;
}

html, body, #app, .app {
  height: 100%;
}

.loading {
  position: absolute;
  top: 1%;
  width: 100%;
}

.f-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

body {
	background: #F2F2F2;
	color: #3d3c3c;
}

.transcript {
	font-size: 48px;
  padding: 50px 150px;
  white-space: break-spaces;
  height: 90vh;
  overflow: auto;
  @media (max-width: 1023px) {
    padding: 50px 30px;
    font-size: 32px;
  }
}

.micContainer {
  position: relative;
  top: -40px;
  display: flex;
  justify-content: center;
	padding: 8px;
  width: 100px;
  :hover {
    cursor: pointer;
  }
  .btn {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: #f32424;
    color: white;
    box-shadow: 0px 0px 0px 6px #40414252;
    :hover {
      cursor: pointer;
    }
  }
}
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  border-radius: 33px 33px 0 0;
  // background-color: #b6babe;
  height: 30px;
}
</style>
