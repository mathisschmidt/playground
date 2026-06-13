import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import HomeView from './views/HomeView.vue'
import DatasetView from './views/DatasetView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/d/:slug', name: 'dataset', component: DatasetView, props: true },
  ],
})

createApp(App).use(router).mount('#app')
