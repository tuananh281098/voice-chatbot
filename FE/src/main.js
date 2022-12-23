import { createApp } from 'vue'
import App from './App.vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(VueAxios, axios)
app.mount('#app');
