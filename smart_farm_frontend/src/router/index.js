/* eslint-disable */
import { createRouter, createWebHistory } from "vue-router";
import Home from "../components/Home.vue";
import Rules from "../components/Rules.vue";
import Settings from "../components/Settings.vue";
import SensorDetails from "../components/SensorDetails.vue";
import ButtonDetails from '@/components/ButtonDetails.vue';
import PIRDetails from '@/components/PIRDetails.vue';
import BuzzerDetails from '@/components/BuzzerDetails.vue';
import LCDDetails from '@/components/LCDDetails.vue';
import ServoDetails from '@/components/ServoDetails.vue';
import LEDDetails from '@/components/LEDDetails.vue';
import RelayDetails from '@/components/RelayDetails.vue';
import FanDetails from '@/components/FanDetails.vue';
import LoginPage from '@/components/LoginPage.vue';

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/home", component: Home },
  { path: "/rules", component: Rules },
  { path: "/settings", component: Settings },
  { path: "/sensor/:title", component: SensorDetails },
  { path: '/button-details', name: 'ButtonDetails', component: ButtonDetails },
  { path: '/pir-details', name: 'PIRDetails', component: PIRDetails },
  { path: '/buzzer-details', name: 'BuzzerDetails', component: BuzzerDetails },
  { path: '/lcd-details', name: 'LCDDetails', component: LCDDetails },
  { path: '/servo-details', name: 'ServoDetails', component: ServoDetails },
  { path: '/led-details', name: 'LEDDetails', component: LEDDetails },
  { path: '/relay-details', name: 'RelayDetails', component: RelayDetails },
  { path: '/fan-details', name: 'FanDetails', component: FanDetails },
  { path: '/login', name: 'LoginPage', component: LoginPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
