<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const apiUrl = "https://voice-chatbot-api.saokhue.io"

const transcript = ref('')
const isRecording = ref(false)

const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition
const sr = new Recognition()
// sr.lang = 'vi-VN';

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
	axios
    .put(apiUrl + `/messages:input?text=${transcript.value}`)
    .then((response) => {
      if (response.status === 200) {
        console.log(response.data)
        transcript.value = response.data.text;
        const audio = new Audio("data:audio/mpeg;base64," + response.data.audio);
        audio.play();
      }
    });
}

const ToggleMic = () => {
	if (isRecording.value) {
		sr.stop()
	} else {
		sr.start()
	}
}
</script>

<template>
	<div class="app">
		<button type="button" :class="`mic`" @click="ToggleMic">
			{{ isRecording ? 'Stop' : 'Record' }}
		</button>
		<div class="transcript" v-text="transcript"></div>
	</div>
</template>

<style>
* {
	margin: 0;
	padding: 0;
	box-sizing: border-box;
	font-family: 'Fira sans', sans-serif;
}

body {
	background: #281936;
	color: #FFF;
}

.transcript {
	font-size: 48px;
    padding: 150px;
}

.mic {
	position: absolute;
    bottom: 5px;
    left: 50%;
	padding: 8px;
}
</style>
