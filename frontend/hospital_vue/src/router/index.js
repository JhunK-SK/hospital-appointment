import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import LogIn from '../views/LogIn.vue'
import SignUp from '../views/SignUp.vue'
import UserControl from '../views/UserControl.vue'
import PatientInfo from '../views/PatientInfo.vue'
import DoctorInfo from '../views/DoctorInfo.vue'
import DoctorList from '../views/DoctorList.vue'
import CreateAppointment from '../views/CreateAppointment.vue'
import UserAppointments from '../views/UserAppointments.vue'
import EditAppointment from '../views/EditAppointment.vue'

import store from '../store/index.js'
import axios from 'axios'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/user-control',
    name: 'UserControl',
    component: UserControl,
    meta: {
      loginRequired: true,
    }
  },
  {
    path: '/patient/:email',
    name: 'PatientInfo',
    component: PatientInfo,
    meta: {
      loginRequired: true,
    },
    props: true,
  },
  {
    path: '/doctor/:email',
    name: 'DoctorInfo',
    component: DoctorInfo,
    meta: {
      loginRequired: true,
    },
    props: true,
  },
  {
    path: '/doctors',
    name: 'DoctorList',
    component: DoctorList,
  },
  {
    path: '/appointment',
    name: 'CreateAppointment',
    component: CreateAppointment,
    meta: {
      loginRequired: true,
    },
  },
  {
    path: '/appointment/edit/:id',
    name: 'EditAppointment',
    component: EditAppointment,
    meta: {
      loginRequired: true,
    },
    props: true,
  },
  {
    path: '/appointment/user',
    name: 'UserAppointments',
    component: UserAppointments,
    meta: {
      loginRequired: true,
    },
    props: true,
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
router.beforeEach((to, from, next) => {
  // go to login page when page is required to login and request user is not logged in
  if(to.matched.some(record => record.meta.loginRequired) && !store.state.isAuthenticated) {
    next('/log-in')
  } else if(to.matched.some(record => record.meta.loginRequired)){
    // set the localStorage every time access to login required page by authenticated user
    // since some pages display information upon localStorage content such as email and user type
    axios.get('/api/users/me/')
    .then(res => {
      const userType = res.data['user_type']
      const email = res.data['email']
      localStorage.setItem('userType', userType)
      localStorage.setItem('email', email)
    })
    next()
  } else {
    next()
  }
})
export default router
